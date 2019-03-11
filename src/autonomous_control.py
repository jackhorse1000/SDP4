"""Generic motor-control module. Provides helper methods for manipulating
   each motor and pairs of motors. Same as control.py but with added safety"""

# pylint: disable=R0401, W0611
# Disable cyclic imports. It's horrible, but I don't want to refactor right now.

import asyncio
import functools
import logging

from typing import Callable, Dict

import motor
from data import SensorData

LOG = logging.getLogger("Control")

DRIVE_RIGHT = 4
DRIVE_LEFT = 5
DRIVE_BACK = 1

SPEED = 255

DRIVE_SIDE_FWD = -SPEED
DRIVE_SIDE_BCK = SPEED

STEP_BACK = 3  # 1 up, -1 down
STEP_FRONT = 2

STEP_FRONT_MIN = -1200 # 1400 Full Extension
STEP_FRONT_MAX = 0 # Normal

STEP_BACK_MIN = -30 # Normal
STEP_BACK_MAX = 1200 # Full Extension

STATES = {} # type: Dict[str, str]
SLEEP = 0.1

def state(*machines: str) -> Callable[[Callable[[], None]], Callable[[], None]]:
    """A decorator, which only applies the underlying function if the given machines
       are not already in this state.

       This can be thought of as a way to emulate basic state-transitions.
    """
    for machine in machines:
        if machine not in STATES:
            STATES[machine] = "_"

    def decorator(func: Callable[[], None]) -> Callable[[], None]:
        new_state = func.__name__

        @functools.wraps(func)
        def worker() -> None:
            changed = False
            # Update the state machine
            for machine in machines:
                if STATES[machine] != new_state:
                    changed = True
                    STATES[machine] = new_state

            # And call if any changes occurred.
            if changed:
                LOG.debug("Running %s", new_state)
                func()

        return worker

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
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_BACK, DRIVE_SIDE_FWD)

@state("drive")
def backward() -> None:
    """Move Spencer backwards."""
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_BACK, DRIVE_SIDE_BCK)

@state("drive")
def turn_left() -> None:
    """Attempt to turn Spencer left. It's a sight for sore eyes."""
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_FWD)

@state("drive")
def turn_right() -> None:
    """Attempt to turn Spencer right. It's not very effective."""
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_BCK)

@state("step_front")
def lower_front() -> None:
    """Moves the front stepper down, to the base position"""
    motor.set_motor(STEP_FRONT, -SPEED)

@state("step_front")
def lift_front() -> None:
    """Moves the front stepper upwards, from the base position"""
    motor.set_motor(STEP_FRONT, SPEED)

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

def climb(data: SensorData) -> None:
    """Tries to climb automatically"""
    from climb import ClimbController
    async def run() -> None:
        # Attempt to normalise the lifting mechanisms to a point so they're no
        # longer touching the ground.
        while data.get_moving():
            lift_both()
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

        for i in range(1):
            LOG.info("Climbing step %d", i+1)
            await ClimbController(data).find_wall()
            # We should return from find wall aligned to the step and as close
            # as we can get before the distance sensors can't read anymore

            # Lift the front mechanism to its upper point
            while data.get_moving():
                lift_front()
                if data.front_lifting_rot.get() <= STEP_FRONT_MIN:
                    # TODO(anyone) Use distance sensors here too - if we can do it reliably.
                    stop()
                    break
                await asyncio.sleep(SLEEP)

            while data.get_moving():
                forward()
                if data.middle_stair_touch.get():
                    stop()
                    break
                await asyncio.sleep(SLEEP)

            # Lower the front mechanism until touching the stair.
            while data.get_moving():
                lower_front()
                if data.front_ground_touch.get() or data.front_lifting_rot.get() >= STEP_FRONT_MAX:
                    stop()
                    break
                await asyncio.sleep(SLEEP)

            # HACK HACK HACK: Ensure the back has a head-start on the front, as it
            #  lifts a little slower.
            if data.get_moving():
                lower_back()
                await asyncio.sleep(0.5)
                stop()

            target_back = -data.front_lifting_rot.get()
            LOG.info("Targeting back lifting of %d", target_back)
            init = False
            while data.get_moving():
                if not init:
                    lower_both()
                    init = True
                # If the back one has reached the stair, then we're all good
                # TODO(anyone): Add distance sensor for back stair
                if data.back_stair_touch.get():
                    LOG.info("Back stair touch hit, finishing climb")
                    stop()
                    break

                if data.front_lifting_rot.get() >= 0:
                    stop_front()
                    forward()

                # TODO(anyone): Reach max extension / max back rotation start going forward
                if (data.back_lifting_rot.get() >= target_back) or data.back_lifting_rot.get() >= STEP_BACK_MAX:
                    stop_back()
                    forward()
                else:
                    lower_back()

                await asyncio.sleep(SLEEP)

            while data.get_moving():
                lift_back()
                # TODO(anyone): Reach normal extension / max back rotation stop
                if data.back_lifting_rot.get() <= STEP_FRONT_MAX:
                    stop()
                    break
                await asyncio.sleep(SLEEP)
            await asyncio.sleep(SLEEP)


    asyncio.get_event_loop().create_task(run())

def downstairs(data: SensorData) -> None:
    """Tries to climb downstairs automatically"""
    async def run() -> None:
        for i in range(1):
            # Backwards until back ground is not touching and we have a reading
            # on the distance sensor
            while data.get_moving():
                backward()
                if not data.back_ground_touch.get() and not data.middle_ground_touch.get():
                    stop()
                    # Check if back ground distance sensor is reading values then
                    # lower back until back ground touch is true
                    if data.back_ground_dist.get() < 20:
                        break
                    else:
                        # TODO(anyone): We need to panic, check we need to handle this better
                        LOG.error("Cannot go downstairs distance to large: %f",
                                  data.back_ground_dist.get())
                        data.set_moving(False)
                await asyncio.sleep(SLEEP)

            while data.get_moving():
                lower_back()
                if data.back_ground_touch.get() or data.back_lifting_rot.get() >= STEP_BACK_MAX:
                    stop()
                    if data.back_lifting_rot.get() >= STEP_BACK_MAX:
                        # We should throw an error because this should not happen
                        LOG.error("Cannot go downstairs. Back is at full extension"
                                   "and can't touch step. rot = %f",
                                  data.back_lifting_rot.get())
                        data.set_moving(False)
                    break
                await asyncio.sleep(SLEEP)

            while data.get_moving():
                backward() # Backward until back stair distance sensor reaches our set limit
                # TODO: We need to make sure this is correct. Made it lower than it was.
                if data.front_ground_dist.valid and data.front_ground_dist.get() > 10:
                    # HACK: There's probably better solutions, but it's the day before the demo and
                    # the only thing stopping me killing Spencer is lack of a credible alibi.
                    await asyncio.sleep(0.5)
                    stop()
                    break
                await asyncio.sleep(SLEEP)

            # Lift both until middle is on the ground
            while data.get_moving():
                lift_both()
                # Check if middle is touching,
                if data.back_lifting_rot.get() <= STEP_BACK_MIN:
                    stop()
                    LOG.error("Cannot go downstairs. Back is at normal"
                              "and middle is not touching step. rot = %f",
                              data.back_lifting_rot.get())
                    data.set_moving(False)
                    break

                if data.front_lifting_rot.get() <= STEP_FRONT_MIN:
                    stop()
                    LOG.error("Cannot go downstairs. Front is at max extension"
                              "and middle is not touching step. rot = %f",
                              data.front_lifting_rot.get())
                    data.set_moving(False)
                    break

                if data.middle_ground_touch.get():
                    stop()
                    break
                await asyncio.sleep(SLEEP)

            # Move back so you can fit front on step
            while data.get_moving():
                backward()
                if not data.back_ground_touch.get():
                    await asyncio.sleep(0.2) # HACK: 
                    stop()
                    break
                await asyncio.sleep(SLEEP)

            # Move back so you can fit front on step
            while data.get_moving():
                lower_front()
                if data.front_ground_touch.get():
                    stop()
                    data.front_lifting_rot.reset()
                    break
                await asyncio.sleep(SLEEP)

            # # Lower back so it is on the step
            # while data.get_moving():
            #     lower_back()
            #     if data.back_lifting_rot.get() >= STEP_BACK_MAX:
            #         stop()
            #         LOG.error("Trying to reset back rot, but rot is max = %f", \
            #                         data.back_lifting_rot.get())
            #         data.set_moving(False)
            #         break

            #     if data.back_ground_touch.get():
            #         # Used to reset the back rotation counter
            #         data.back_lifting_rot.reset()
            #         stop()
            #         break
            #     await asyncio.sleep(SLEEP)

            # if data.get_moving():
            #     backward() #TODO(anyone): review and change
            #     while True:
            #         if not data.back_ground_touch.get():
            #             stop()
            #             break
            #         # Used for last step
            #         # TODO: Will need changed
            #         if i == 1:
            #             await asyncio.sleep(2)
            #             stop()
            #             break
            #         await asyncio.sleep(SLEEP)

            # # Lower front until it is touching the step
            # while data.get_moving():
            #     lower_front()

            #     if data.front_lifting_rot.get() >= STEP_FRONT_MAX:
            #         stop()
            #         LOG.error("Trying to reset front rot, but rot is max = %f", \
            #                         data.front_lifting_rot.get())
            #         data.set_moving(False)
            #         break

            #     if data.front_ground_touch.get():
            #         # Used to reset the front rotation counter
            #         data.front_lifting_rot.reset()
            #         stop()
            #         break
            #     await asyncio.sleep(SLEEP)

        await asyncio.sleep(SLEEP)

    asyncio.get_event_loop().create_task(run())

async def zero(data: SensorData) -> None:
    """Zeros out the rotation sensors. We attempt to move the front and back
       lifting mechanisms to the bottom position, and then reset them to
       0.

    """
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
