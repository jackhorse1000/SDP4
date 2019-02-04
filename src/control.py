"""Generic motor-control module. Provides helper methods for manipulating
   each motor and pairs of motors."""

import motor

DRIVE_RIGHT = 5 # 1 back, -1 forewards
DRIVE_LEFT = 4  # 1 back, -1 forewards
DRIVE_BACK = 1 # No clue

DRIVE_SIDE_FWD = -100
DRIVE_SIDE_BCK = 100

STEP_BACK = 3   # 1 up, -1 down
STEP_FRONT = 2

def stop():
    """Stop all motors.

       Note, there is a slight chance that any motor commands immediately
       after this one may be discarded, so it may be advisable to sleep
       after using this.

    """
    motor.stop_motors()

def forward():
    """Move Spencer forwards."""
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_BACK, DRIVE_SIDE_FWD)

def backward():
    """Move Spencer backwards."""
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_BACK, DRIVE_SIDE_BCK)

def turn_left():
    """Attempt to turn Spencer left. It's a sight for sore eyes."""
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_FWD)

def turn_right():
    """Attempt to turn spencer right. It's not very effective."""
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_BCK)

def lower_front():
    """Moves the front stepper down, to the base position"""
    motor.set_motor(STEP_FRONT, -100)

def lift_front():
    """Moves the front stepper upwards, from the base position"""
    motor.set_motor(STEP_FRONT, 100)

def lower_back():
    """Moves the back stepper down, from the base position"""
    motor.set_motor(STEP_BACK, -100)

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
