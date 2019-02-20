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

async def climb_upstairs():
    """ Function to make Spencer start climbing up stairs"""
    # TODO(anyone): Stop all movement
    # TODO(anyone): SAFETY CHECKS STILL NEED TO BE DONE
    
    # TODO(anyone): Need to sense step
    # TODO(anyone): Use Jonathan's code to align

    # BE INFRONT OF THE STEP
    # Spencer is infront of a step, TODO(anyone): Check
    touching_step = False
    while not touching_step:
        if SensorData.front_stair_touch.get_value() == 1:
            # We are touching the step we can continue
            touching_step = True
            stop()
        else:
            # TODO(anyone) Align step keep driving forward until we reach step
            
    
    # LIFT FRONT ABOVE STEP
    # TODO(anyone): Lift front until max or touch sensor is 0
    front_above_step = False
    while not front_above_step:
        if SensorData.front_stair_touch == 0 and SensorData.front_lifting_normal == 0 and SensorData.front_dist_0 >= 20 and SensorData.front_dist_1 >= 20:
            # The front is above the step
            front_above_step = True
            stop()
        else:
            # The front is not above the step we need to continue
            # TODO(anyone): Lift the front more

    # PLACE FRONT ON STEP
    # TODO(anyone): Drive forward so middle is touching the step
    front_on_step = False
    while not front_on_step:
        if SensorData.front_ground_touch == 1 and SensorData.front_lifting_normal == 0 and SensorData.front_middle_stair_touch == 1:
            # Front is on the step we can continue
            front_on_step = True
        else:
            # Front is not on the step we need to drive forward or lower the front more
            if SensorData.front_middle_stair_touch == 1:
                # Middle is touching the step
                # TODO(anyone): Lower the front until touching the step
                stop()
            else:
                # TODO(anyone): Drive forward until Middle is touching the step

    # TODO(anyone): Lower Both until front in normal or back is max
    max_movement = False
    while not max_movement:
        if SensorData.front_lifting_normal == 1 and SensorData.back_lifting_extended_max == 0:
            # The robot has moved the maximum it can for either lifting mechanism
            max_movement = True
            stop()
        else:
            #TODO(anyone): Continue to lift the robot up

    # TODO(anyone): Drive forward so middle is on the step
    """ This bit can be quite tricky, if we still have the falling problem, we may need to lift
        one of the lifting mechanisms. We will need to do this while driving forward. Until we have
        met the conditions for being on the step """
    on_step = False
    while not on_step:
        if SensorData.front_ground_touch == 1 and SensorData.middle_ground_touch == 1 and SensorData.back_stair_touch == 1:
            # The robot is on the step
            on_step = True
            stop()
        else:
          # The robot is not on the step
          # TODO(anyone): Drive forward and keep the lifting mechanisms at the limits of extension

    # TODO(anyone): Lift back until in normal position
    is_back_normal = False
    while not is_back_normal:
          if SensorData.back_lifting_normal == 1:
              # Back is normal
              is_back_normal = True
              stop()
          else:
              # TODO(anyone): Continue lifting back until normal


    # TODO(anyone): Repeat above until at the top of the stairs

    return

def on_stair():
    """ Function to check if the robot satisfies the condition to be on a step """

async def climb_downstairs():
    """ Function to make Spencer start climbing downstairs"""
    # TODO(anyone): Stop step climbing thread
    return

def climb_a_stair():
    """ Function to make Spencer climb a step """
    # TODO(anyone): Stop step climbing thread
    return
