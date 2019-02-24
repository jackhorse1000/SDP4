"""Generic motor-control module. Provides helper methods for manipulating
   each motor and pairs of motors. Same as control.py but with added safety"""

import asyncio
import functools
import logging
from typing import Callable, Dict

import motor
from data import SensorData as data

LOG = logging.getLogger("Control")

DRIVE_RIGHT = 5
DRIVE_LEFT = 4
DRIVE_BACK = 1

DRIVE_SIDE_FWD = -100
DRIVE_SIDE_BCK = 100

STEP_BACK = 3  # 1 up, -1 down
STEP_FRONT = 2

STATES = {} # type: Dict[str, str]

def state(*machines: str) -> Callable[[Callable[[], None]], Callable[[], None]]:
    """A decorator, which only applies the underlying function if the given machines
       are not already in this state.

       This can be thought of as a way to emulate basic state-transitions.
    """
    def decorator(func: Callable[[], None]) -> Callable[[], None]:
        new_state = func.__name__

        @functools.wraps(func)
        def worker() -> None:
            changed = False
            # Update the state machine
            for machine in machines:
                if machine not in STATES or STATES[machine] != new_state:
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

# TODO(anyone): NEED TO ADD SAFETY TO EVERYTHING

async def poll_forward():
    """Stops moving forward if the front sensor is triggered."""
    while True:
        if "drive" in STATES and STATES["drive"] == "forward" and data.front_stair_touch.get():
            stop()
        
        if "drive" in STATES and STATES["drive"] == "forward" and data.front_middle_stair_touch.get() and (not data.front_lifting_extended_max.get() or data.front_lifting_normal.get()):
            stop()

        await asyncio.sleep(0.05)

async def poll_lift_front():
    """Stops moving forward if the front sensor is triggered."""
    while True:
        if "step_front" in STATES and STATES["step_front"] == "lift_front" and not data.front_lifting_extended_max.get():
            stop()

        await asyncio.sleep(0.05)

async def poll_lower_front():
    """Stops moving forward if the front sensor is triggered."""
    while True:
        if "step_front" in STATES and STATES["step_front"] == "lower_front" and data.front_ground_touch.get():
            stop()

        await asyncio.sleep(0.05)

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

def lower_both() -> None:
    """Lower both the front and back motors."""
    lower_back()
    lower_front()

def lift_both() -> None:
    """Lift both the front and back motors."""
    lift_back()
    lift_front()
