"""Generic motor-control module. Provides helper methods for manipulating
   each motor and pairs of motors. Same as control.py but with added safety"""

import asyncio
import functools
import logging
import time

from typing import Callable, Dict

import motor
from data import SensorData as data

LOG = logging.getLogger("Control")

DRIVE_RIGHT = 4
DRIVE_LEFT = 5
DRIVE_BACK = 1

DRIVE_SIDE_FWD = -100
DRIVE_SIDE_BCK = 100

STEP_BACK = 3  # 1 up, -1 down
STEP_FRONT = 2

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

@state("step_front", "step_back", "drive", "climb")
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

@state("step_back")
def lower_back() -> None:
    """Moves the back stepper down, from the base position"""
    motor.set_motor(STEP_BACK, -100)

@state("step_back")
def lift_back() -> None:
    """Moves the back stepper upwards, to the base position"""
    motor.set_motor(STEP_BACK, 100)

@state("climb")
def lower_both() -> None:
    """Lower both the front and back motors."""
    motor.set_motor(STEP_BACK, -100)
    motor.set_motor(STEP_FRONT, -100)

@state("climb")
def lift_both() -> None:
    """Lift both the front and back motors."""
    motor.set_motor(STEP_BACK, 100)
    motor.set_motor(STEP_FRONT, 100)

def climb() -> None:
    """Tries to climb automatically"""
    async def run():
        import climb
        climb = climb.ClimbController(data)
        await climb.find_wall()

        forward()
        while True:
            if data.front_stair_touch.get():
                stop()
                break
            await asyncio.sleep(SLEEP)

        lift_front()
        while True:
            if ((not data.front_stair_touch.get() and data.front_dist_0.get() > 20 and data.front_dist_1.get() > 20)):
                # or not data.front_lifting_extended_max.get()
                stop()
                break
            await asyncio.sleep(SLEEP)

        forward()
        while True:
            if data.front_middle_stair_touch.get():
                stop()
                break
            await asyncio.sleep(SLEEP)

        lower_front()
        while True:
            if data.front_ground_touch.get(): # or data.front_lifting_normal.get()):
                stop()
                break
            await asyncio.sleep(SLEEP)

        # HACK HACK HACK
        lower_back()
        await asyncio.sleep(2)
        stop()

        lower_both()
        while True:
            if not data.front_lifting_normal.get():
                motor.stop_motor(STEP_FRONT)
                forward()
            if data.back_lifting_extended_max.get():
                # TODO(anyone): Add distance sensor for back stair
                motor.stop_motor(STEP_BACK)
                forward()
            if data.back_lifting_extended_max.get() and not data.front_lifting_normal.get() \
                or data.back_stair_touch.get():
                stop()
                break
            await asyncio.sleep(SLEEP)

        forward()
        while True:
            if data.back_stair_touch.get():
                stop()
                break
            await asyncio.sleep(SLEEP)

        # lift_both()
        # while True:
        #     if data.front_lifting_extended_max.get():
        #         stop()
        #         break
        #     await asyncio.sleep(SLEEP)

        lift_back()
        while True:
            if data.back_lifting_normal.get():
                stop()
                break
            await asyncio.sleep(SLEEP)
        await asyncio.sleep(2)


    asyncio.get_event_loop().create_task(run())
