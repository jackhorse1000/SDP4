"""Generic motor-control module. Provides helper methods for manipulating
   each motor and pairs of motors. Same as control.py but with added safety"""

# pylint: disable=R0401
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

DRIVE_SIDE_FWD = -100
DRIVE_SIDE_BCK = 100

STEP_BACK = 3  # 1 up, -1 down
STEP_FRONT = 2

STEP_FRONT_MIN = -1200 # -1400

STEP_BACK_MIN = -200
STEP_BACK_MAX = 1400

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

@state("step_front") # TODO Merge this into the climb stage??
def lower_front() -> None:
    """Moves the front stepper down, to the base position"""
    motor.set_motor(STEP_FRONT, -100)

@state("step_front")
def lift_front() -> None:
    """Moves the front stepper upwards, from the base position"""
    motor.set_motor(STEP_FRONT, 100)

@state("step_front")
def stop_front() -> None:
    """Stops the front stepper"""
    motor.stop_motor(STEP_FRONT)

@state("step_back")
def lower_back() -> None:
    """Moves the back stepper down, from the base position"""
    motor.set_motor(STEP_BACK, 100)

@state("step_back")
def lift_back() -> None:
    """Moves the back stepper upwards, to the base position"""
    motor.set_motor(STEP_BACK, -100)

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
    async def run() -> None:
        # from climb import ClimbController
        # await ClimbController(data).find_wall()
        # We should return from find wall aligned to the step and as close as we can get before the
        # distance sensors can't read anymore

        # forward()  # Forward for x seconds, this needs to be determined
        # while True:
        #     # TODO(anyone): Find time to go forward
        #     await asyncio.sleep(2)
        #     stop()
        #     break

        lift_front()
        while True:
            if data.front_lifting_rot.get() <= STEP_FRONT_MIN:
                # TODO(anyone) Use distance sensors here too - if we can do it reliably.
                stop()
                break
            await asyncio.sleep(SLEEP)

        forward()
        while True:
            if data.middle_stair_touch.get():
                stop()
                break
            await asyncio.sleep(SLEEP)

        lower_front()
        while True:
            if data.front_ground_touch.get() or data.front_lifting_rot.get() >= 0:
                stop()
                break
            await asyncio.sleep(SLEEP)

        # HACK HACK HACK
        lower_back()
        await asyncio.sleep(1)
        stop()

        target_back = -data.front_lifting_rot.get()
        LOG.info("Targeting back lifting of %d", target_back)
        lower_both()
        while True:
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
            if data.back_lifting_rot.get() >= target_back + 200:
                stop_back()
                forward()
            else:
                lower_back()

            await asyncio.sleep(SLEEP)

        lift_back()
        while True:
            # TODO(anyone): Reach normal extension / max back rotation stop
            if data.back_lifting_rot.get() <= 0:
                stop()
                break
            await asyncio.sleep(SLEEP)
        await asyncio.sleep(2)


    asyncio.get_event_loop().create_task(run())

def climb_downstairs(data: SensorData) -> None:
    """Tries to climb downstairs automatically"""
    async def run() -> None:

        # TODO(anyone): Backwards until back ground is not touching and we have a reading
        # on the distance sensor
        backward()
        while True:
            if not data.back_ground_touch.get():
                stop()
                # TODO(anyone: Check if back ground distance sensor is reading values
                # then lower back until back ground touch is true
            await asyncio.sleep(SLEEP)

        backward() # Backward until back stair distance sensor reaches our set limit
        while True:
            if data.back_stair_dist.get() > 20.5: # TODO(anyone): Update and check value
                stop()
                break
            await asyncio.sleep(SLEEP)

        # Lift both until middle is on the ground
        lift_both()
        while True:
            # Check if middle is touching,
            if data.middle_ground_touch.get():
                stop()
                break
            await asyncio.sleep(SLEEP)

        # Lower back so it is on the step
        lower_back()
        while True:
            if data.back_ground_touch.get():
                # TODO(anyone): Could be used to reset rotation counter
                stop()
                break

        # TODO(anyone): Backwards until back ground is not touching
        backward()
        while True:
            if not data.back_ground_touch.get():
                stop()
                break
            await asyncio.sleep(SLEEP)

        # Lower front until it is touching the step
        lower_front()
        while True:
            if data.front_ground_touch.get():
                # TODO(anyone): Could be used to reset rotation counter
                stop()
                break
            await asyncio.sleep(SLEEP)

        await asyncio.sleep(2)

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
