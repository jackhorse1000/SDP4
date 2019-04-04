"""Generic motor-control module. Provides helper methods for manipulating
   each motor and pairs of motors. Same as control.py but with added safety"""

# pylint: disable=R0401, W0611, too-many-branches
# Disable cyclic imports. It's horrible, but I don't want to refactor right now.

import asyncio
import functools
import logging
import time
from typing import Any, Callable, Coroutine, Dict, TypeVar, cast

import motor
from data import SensorData

LOG = logging.getLogger("Control")

DRIVE_RIGHT = 4
DRIVE_LEFT = 5
DRIVE_BACK = 1
DRIVE_FWD = 0
SPEED = 255

DRIVE_SIDE_FWD = -SPEED
DRIVE_SIDE_BCK = SPEED

STEP_BACK = 3  # 1 up, -1 down
STEP_FRONT = 2

STEP_FRONT_MIN = -1300 # 1400 Full Extension # FIXME: Was 1200 before. Make sure this doesn't screw the pooch.
STEP_FRONT_MAX = -50 # Normal

STEP_BACK_MIN = -100 # Normal
STEP_BACK_MAX = 1300 # Full Extension

STATES = {} # type: Dict[str, str]
SLEEP = 0.1

StateF = TypeVar('StateF', bound=Callable[..., None])

ProgressCallback = Callable[[str], None]

def state(*machines: str) -> Callable[[StateF], StateF]:
    """A decorator, which only applies the underlying function if the given machines
       are not already in this state.

       This can be thought of as a way to emulate basic state-transitions.
    """
    for machine in machines:
        if machine not in STATES:
            STATES[machine] = "_"

    def decorator(func: StateF) -> StateF:
        new_state = func.__name__

        @functools.wraps(func)
        def worker(*args, **kwargs):
            changed = False
            # Update the state machine
            for machine in machines:
                if STATES[machine] != new_state:
                    changed = True
                    STATES[machine] = new_state

            # And call if any changes occurred.
            if changed:
                LOG.debug("Running %s", new_state)
                func(*args, **kwargs)

        return cast(StateF, worker)

    return decorator

@state("step_front", "step_back", "drive")
def stop() -> None:

    """Stop all motors.

       Note, there is a slight chance that any motor commands immediately
       after this one may be discarded, so it may be advisable to sleep
       after using this.

    """
    LOG.info("Stopping motors")
    motor.stop_motors()

@state("drive")
def forward() -> None:
    """Move Spencer forwards."""
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_BACK, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_FWD, DRIVE_SIDE_FWD)

@state("drive")
def stop_forward() -> None:
    """Stop Spencer moving forwards."""
    motor.stop_motor(DRIVE_LEFT)
    motor.stop_motor(DRIVE_RIGHT)
    motor.stop_motor(DRIVE_BACK)
    motor.stop_motor(DRIVE_FWD)

@state("drive")
def backward() -> None:
    """Move Spencer backwards."""
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_BACK, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_FWD, DRIVE_SIDE_BCK)

@state("drive")
def turn_left(speed: float = 1.0) -> None:
    """Attempt to turn Spencer left. It's a sight for sore eyes."""
    motor.set_motor(DRIVE_LEFT, int(DRIVE_SIDE_FWD * speed)) # TODO: Fix this so it's actually bloody correct.
    motor.set_motor(DRIVE_RIGHT, int(DRIVE_SIDE_FWD * speed))

@state("drive")
def turn_right(speed: float = 1.0) -> None:
    """Attempt to turn Spencer right. It's not very effective."""
    motor.set_motor(DRIVE_LEFT, int(DRIVE_SIDE_BCK * speed))
    motor.set_motor(DRIVE_RIGHT, int(DRIVE_SIDE_BCK * speed))

@state("step_front")
def lower_front() -> None:
    """Moves the front stepper down, to the base position"""
    motor.set_motor(STEP_FRONT, SPEED)

@state("step_front")
def lift_front() -> None:
    """Moves the front stepper upwards, from the base position"""
    motor.set_motor(STEP_FRONT, -SPEED)

@state("step_front")
def stop_front() -> None:
    """Stops the front stepper"""
    motor.stop_motor(STEP_FRONT)

@state("step_back")
def lower_back() -> None:
    """Moves the back stepper down, from the base position"""
    motor.set_motor(STEP_BACK, SPEED)

@state("step_back")
def lift_back() -> None:
    """Moves the back stepper upwards, to the base position"""
    motor.set_motor(STEP_BACK, -SPEED)

@state("step_back")
def stop_back() -> None:
    """Stops the back stepper"""
    motor.stop_motor(STEP_BACK)

def lower_both() -> None:
    """Lower both the front and back motors."""
    lower_back()
    lower_front()

def lift_both() -> None:
    """Lift both the front and back motors."""
    lift_back()
    lift_front()

def at_top_of_stairs(data: SensorData) -> bool:
    """ Check to see if the robot is at the top of the stairs """
    return ((data.front_dist_0.value > 20 or not data.front_dist_0.valid) and
            (data.front_dist_1.value > 20 or not data.front_dist_1.valid))

def climb_(data: SensorData, callback: ProgressCallback) -> Callable[[], Coroutine[Any, Any, None]]:
    """Returns a worker which will climb upstairs."""

    def obstacle_infront() -> bool:
        """ Detects if there is an obstacle in front of the robot """
        if not data.front_dist_1.valid and not data.front_dist_0.valid:
            return False
        if (abs(data.front_dist_0.value - data.front_dist_1.value) > 5
                and min(data.front_dist_0.value, data.front_dist_1.value) <= 20):
            LOG.info("Obstacle in front of Spencer, dist_0 = %f, dist_1=%f",
                     data.front_dist_0.value, data.front_dist_1.value)
            return True
        return False

    from climb import ClimbController
    async def run() -> None:
        step_count = 0
        if at_top_of_stairs(data):
            LOG.error("At the top of the stairs on the initial climb. This is as useful as a chocolate teapot.")

        while not at_top_of_stairs(data) and data.get_moving():
            step_count += 1
            LOG.info("Climbing step %d", step_count)
            callback("Climbing step %d (finding stair)" % step_count)

            lift_both()
            while data.get_moving():
                front, back = False, False
                if data.front_lifting_rot.get() <= -100:
                    stop_front()
                    front = True

                if data.back_lifting_rot.get() <= -30:
                    stop_back()
                    back = True
                if front and back:
                    break
                await asyncio.sleep(SLEEP)

            # We should return from find wall aligned to the step and as close
            # as we can get before the distance sensors can't read anymore
            await ClimbController(data).find_wall()

            # Lift the front mechanism to its upper point
            callback("Climbing step %d (lifting front)" % step_count)
            while data.get_moving():
                lift_front()
                if data.front_lifting_rot.get() <= STEP_FRONT_MIN:
                    stop()
                    break
                await asyncio.sleep(SLEEP)

            while data.get_moving():
                forward()
                if obstacle_infront():
                    stop_forward()
                    await asyncio.sleep(0.5)
                else:
                    forward()
                if data.middle_stair_touch.get():
                    stop()
                    break
                await asyncio.sleep(SLEEP)

            # Lower the front mechanism until touching the stair.
            callback("Climbing step %d (touching off front)" % step_count)
            while data.get_moving():
                lower_front()
                if data.front_ground_touch.get() or data.front_lifting_rot.get() >= STEP_FRONT_MAX:
                    stop()
                    break
                await asyncio.sleep(SLEEP)

            callback("Climbing step %d (climbing)" % step_count)

            # HACK HACK HACK: Ensure the back has a head-start on the front, as it
            #  lifts a little slower.
            if data.get_moving():
                lower_back()
                await asyncio.sleep(0.5)
                stop()

            target_back = -data.front_lifting_rot.get() + 50
            LOG.info("Targeting back lifting of %d", target_back)
            init = False
            while data.get_moving():
                if not init:
                    lower_both()
                    init = True
                # If the back one has reached the stair, then we're all good
                # TODO(anyone): Add distance sensor for back stair
                # was using data.back_stair_touch.get()
                # if data.middle_ground_touch.get():
                #     LOG.info("Back stair touch hit, finishing climb")
                #     stop()
                #     break

                if data.front_lifting_rot.get() >= 0:
                    if data.middle_ground_touch.get():
                        LOG.info("Back stair touch hit, finishing climb")
                        stop()
                        break
                    stop_front()
                else:
                    lower_front()

                # TODO(anyone): Reach max extension / max back rotation start going forward
                if data.back_lifting_rot.get() >= target_back or data.back_lifting_rot.get() >= STEP_BACK_MAX:
                    stop_back()
                    forward()
                    # Detect if obstacle is in front and stop
                    if obstacle_infront():
                        stop_forward()
                        await asyncio.sleep(0.25)

                    if data.middle_ground_touch.get():
                        LOG.info("Back stair touch hit, finishing climb")
                        stop()
                        break
                else:
                    lower_back()


            callback("Climbing step %d (lifting back)" % step_count)
            while data.get_moving():
                lift_back()
                if data.back_lifting_rot.get() <= STEP_BACK_MIN:
                    stop()
                    break
                await asyncio.sleep(SLEEP)

            await asyncio.sleep(SLEEP)

        while data.get_moving():
            lift_back()
            if data.back_lifting_rot.get() <= STEP_BACK_MIN:
                stop()
                break
            await asyncio.sleep(SLEEP)

        forward()
        await asyncio.sleep(1)
        stop()

        callback("Idle")

    return run

def downstairs_(data: SensorData, callback: ProgressCallback) -> Callable[[], Coroutine[Any, Any, None]]:
    """Returns a worker which will climb downstairs"""
    from climb import ClimbController
    async def run() -> None:
        is_at_bottom_of_stairs = False
        step_count = 0
        while not is_at_bottom_of_stairs and data.get_moving():
            step_count += 1
            LOG.info("Descending step %d", step_count)
            callback("Descending step %d (finding stair)" % step_count)

            # Backwards until back ground is not touching and we have a reading
            # on the distance sensor
            while data.get_moving():
                backward()
                if not data.back_ground_touch.get() and not data.middle_ground_touch.get():
                    stop()
                    break
                await asyncio.sleep(SLEEP)

            while data.get_moving:
                lower_front()
                if data.front_ground_touch.get():
                    stop_front()
                    break
                await asyncio.sleep(SLEEP)

            # Try and align with stairs if off
            if step_count != 1:
                await ClimbController(data).downstairs_find_wall()

            callback("Descending step %d (lowering back)" % step_count)
            while data.get_moving:
                lower_back()
                if data.back_ground_touch.get() or data.back_lifting_rot.get() >= STEP_BACK_MAX:
                    stop_back()
                    break
                await asyncio.sleep(SLEEP)

            while data.get_moving():
                backward() # Backward until back stair distance sensor reaches our set limit
                # TODO: We need to make sure this is correct. Made it lower than it was.
                if data.front_ground_dist.valid and data.front_ground_dist.get() > 9:
                    # HACK: There's probably better solutions, but it's the day before the demo and
                    # the only thing stopping me killing Spencer is lack of a credible alibi.
                    await asyncio.sleep(0.7)
                    stop()
                    break
                await asyncio.sleep(SLEEP)

            # HACK HACK HACK: Ensure the front has a head-start on the back, as it
            #  moves a little slower.
            if data.get_moving():
                lift_front()
                await asyncio.sleep(0.5)
                stop()

            # Lift both until middle is on the ground
            callback("Descending step %d (lowering)" % step_count)
            while data.get_moving():
                lift_both()

                if data.middle_ground_touch.get():
                    # The robot is at an angle when it lower's downstairs, I added a wait to make it less so
                    await asyncio.sleep(0.35)
                    stop()
                    break

                # Check if middle is touching,
                if data.back_lifting_rot.get() <= STEP_BACK_MIN + 100:
                    stop()
                    LOG.error("Cannot go downstairs. Back is at normal" \
                              "and middle is not touching step. rot = %f", \
                              data.back_lifting_rot.get())
                    # data.set_moving(False)
                    break

                if data.front_lifting_rot.get() <= STEP_FRONT_MIN:
                    stop()
                    LOG.error("Cannot go downstairs. Front is at max extension "
                              "and middle is not touching step. rot = %f",
                              data.front_lifting_rot.get())
                    data.set_moving(False)
                    break

                await asyncio.sleep(SLEEP)

            # Move back so you can fit front on step
            start_time = time.time()
            callback("Descending step %d (finishing off)" % step_count)
            while data.get_moving():
                backward()
                # To determine if Spencer is at the bottom of the stairs
                if time.time() - start_time > 3:
                    is_at_bottom_of_stairs = True
                    data.set_moving(False)
                    stop()
                    break
                LOG.debug("Backwards %ds", time.time() - start_time)
                if not data.back_ground_touch.get() and not data.middle_ground_touch.get():
                    await asyncio.sleep(0.15) # HACK
                    stop()
                    break
                await asyncio.sleep(SLEEP)
        await zero(data, callback)
        await asyncio.sleep(SLEEP)
        callback("Idle")

    return run

def climb(data: SensorData, callback: ProgressCallback) -> None:
    """Tries to climb upstairs automatically"""
    asyncio.get_event_loop().create_task(climb_(data, callback)())

def downstairs(data: SensorData, callback: ProgressCallback) -> None:
    """Tries to climb downstairs automatically"""
    asyncio.get_event_loop().create_task(downstairs_(data, callback)())

async def zero(data: SensorData, callback: ProgressCallback) -> None:
    """Zeros out the rotation sensors. We attempt to move the front and back
       lifting mechanisms to the bottom position, and then reset them to
       0.

    """
    callback("Resetting motors")

    if not data.front_ground_touch.get():
        lower_front()
        while not data.front_ground_touch.get():
            await asyncio.sleep(SLEEP)
        stop()

    if not data.back_ground_touch.get():
        lower_back()
        while not data.back_ground_touch.get():
            await asyncio.sleep(SLEEP)
        stop()

    data.front_lifting_rot.reset()
    data.back_lifting_rot.reset()
    LOG.info("Zeroed lifting mechanisms")

    callback("Idle")

def timed(data: SensorData, callback: ProgressCallback) -> None:
    """Goes upstairs and downstairs, then prints out the times"""
    async def run() -> None:
        start = time.time()
        await climb_(data, callback)()
        LOG.info("upstairs %f", time.time() - start)

        await asyncio.sleep(3)

        start = time.time()
        await downstairs_(data, callback)()
        LOG.info("down %f", time.time() - start)

    asyncio.get_event_loop().create_task(run())

def hello(data: SensorData) -> None:
    """Makes Spencer say hello!"""
    async def run() -> None:
        turn_left()
        await asyncio.sleep(1.0)
        while data.get_moving():
            turn_right()
            await asyncio.sleep(2.0)
            turn_left()
            await asyncio.sleep(2.0)

    asyncio.get_event_loop().create_task(run())
