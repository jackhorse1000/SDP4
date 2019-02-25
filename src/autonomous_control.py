"""Generic motor-control module. Provides helper methods for manipulating
   each motor and pairs of motors. Same as control.py but with added safety"""

import asyncio
import functools
import logging
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

async def state_limiter():
    """Stops various sensors when we hit specific conditions"""
    while True:
        # TODO(anyone): NEED TO ADD SAFETY TO EVERYTHING

        # Stop moving forward if we ever hit the front touch sensor
        if STATES["drive"] == "forward" and data.front_stair_touch.get():
            stop()

        # Stop moving forward if the middle chassis button is touching and we're not extended
        if STATES["drive"] == "forward" and data.front_middle_stair_touch.get() and not data.front_lifting_extended_max.get():
            stop()
        
        # Stop moving forward if the back chassis button is touching and are extended
        if STATES["drive"] == "forward" and data.back_stair_touch.get():
            stop()

        # Stop lifting the front when the maximum flag is set
        if STATES["step_front"] == "lift_front" and not data.front_lifting_extended_max.get():
            stop()

        # Stop lowering the front when it hits the ground
        if STATES["step_front"] == "lower_front" and data.front_ground_touch.get():
            stop()

        # Stop lowering both when the front has reached its default position
        if STATES["climb"] == "lower_both" and (not data.front_lifting_normal.get() or data.back_lifting_extended_max):
            stop()
        
        # Stop lifting both when the middle has touched the ground
        if STATES["climb"] == "lift_both" and data.middle_ground_touch.get():
            stop()
        
        # Stop lifting both when the middle has touched the ground
        if STATES["step_back"] == "lift_back" and data.back_lifting_normal.get():
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
        # import climb
        # climb = climb.ClimbController(data)
        # await climb.find_wall()

        # forward()
        # while STATES["drive"] != "stop":
        #     await asyncio.sleep(0.1)

        # lift_front()
        # while STATES["step_front"] != "stop":
        #     await asyncio.sleep(0.1)

        # forward()
        # while STATES["drive"] != "stop":
        #     await asyncio.sleep(0.1)

        # lower_front()
        # while STATES["step_front"] != "stop":
        #     await asyncio.sleep(0.1)

        lower_both()
        while STATES["climb"] != "stop":
            await asyncio.sleep(0.1)

        forward()
        while STATES["drive"] != "stop":
            await asyncio.sleep(0.1)
        
        lift_both()
        while STATES["climb"] != "stop":
            await asyncio.sleep(0.1)
        
        lift_back()
        while STATES["step_back"] != "stop":
            await asyncio.sleep(0.1)
        await asyncio.sleep(2)


    asyncio.get_event_loop().create_task(run())
