"""Generic motor-control module. Provides helper methods for manipulating
   each motor and pairs of motors."""

import functools
import logging

import motor
from data import SensorData

LOG = logging.getLogger("Control")

DRIVE_RIGHT = 5
DRIVE_LEFT = 4
DRIVE_BACK = 1

DRIVE_SIDE_FWD = -100
DRIVE_SIDE_BCK = 100

STEP_BACK = 3  # 1 up, -1 down
STEP_FRONT = 2

STATES = {}

def state(*machines):
    """A decorator, which only applies the underlying function if the given machines
       are not already in this state.

       This can be thought of as a way to emulate basic state-transitions.
    """
    def decorator(func):
        new_state = func.__name__

        @functools.wraps(func)
        def worker():
            changed = False
            # Update the state machine
            for machine in machines:
                if machine not in STATES or STATES[machine] != new_state:
                    changed = True
                    STATES[machine] = new_state

            # And call if any changes occurred.
            if changed:
                LOG.debug("Running %s", new_state)
                # func()

        return worker

    return decorator

@state("step_front", "step_back", "drive")
def stop():

    """Stop all motors.

       Note, there is a slight chance that any motor commands immediately
       after this one may be discarded, so it may be advisable to sleep
       after using this.

    """
    motor.stop_motors()
    # TODO(anyone): Stop threads here???

@state("drive")
def forward():
    """Move Spencer forwards."""
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_BACK, DRIVE_SIDE_FWD)

@state("drive")
def backward():
    """Move Spencer backwards."""
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_BACK, DRIVE_SIDE_BCK)

@state("drive")
def turn_left():
    """Attempt to turn Spencer left. It's a sight for sore eyes."""
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_FWD)

@state("drive")
def turn_right():
    """Attempt to turn spencer right. It's not very effective."""
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_BCK)

@state("step_front")
def lower_front():
    """Moves the front stepper down, to the base position"""
    motor.set_motor(STEP_FRONT, -100)

@state("step_front")
def lift_front():
    """Moves the front stepper upwards, from the base position"""
    motor.set_motor(STEP_FRONT, 100)

@state("step_back")
def lower_back():
    """Moves the back stepper down, from the base position"""
    motor.set_motor(STEP_BACK, -100)

@state("step_back")
def lift_back():
    """Moves the back stepper upwards, to the base position"""
    motor.set_motor(STEP_BACK, 100)

def lower_both():
    """Lower both the front and back motors."""
    lower_back()
    lower_front()

def lift_both():
    """Lift both the front and back motors."""
    lift_back()
    lift_front()

def climb_upstairs():
    """ Function to make Spencer start climbing up stairs"""
    # TODO(anyone): Stop step climbing thread
    return

def climb_downstairs():
    """ Function to make Spencer start climbing downstairs"""
    # TODO(anyone): Stop step climbing thread
    return

def climb_a_stair():
    """ Function to make Spencer climb a step """
    # TODO(anyone): Stop step climbing thread
    return
