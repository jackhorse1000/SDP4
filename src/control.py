import time

import motor

DRIVE_RIGHT = 5 # 1 back, -1 forewards
DRIVE_LEFT = 4  # 1 back, -1 forewards
DRIVE_BACK = 1 # No clue

DRIVE_SIDE_FWD = -100
DRIVE_SIDE_BCK = 100

STEP_BACK = 3   # 1 up, -1 down
STEP_FRONT = 2

def stop():
    motor.stop_motors()

def forward():
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_BACK, DRIVE_SIDE_FWD)

def backward():
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_BACK, DRIVE_SIDE_BCK)

def turn_left():
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_BCK)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_FWD)

def turn_right():
    motor.set_motor(DRIVE_LEFT, DRIVE_SIDE_FWD)
    motor.set_motor(DRIVE_RIGHT, DRIVE_SIDE_BCK)

def lower_front():
    """Moves the front stepper down, to the base position"""
    motor.set_motor(STEP_FRONT, -100)

def lift_front():
    """Moves the front stepper upwards, from the base position"""
    motor.set_motor(STEP_FRONT, 100)

def lower_back():
    """Moves the back stepper down, to the base position"""
    motor.set_motor(STEP_BACK, -100)

def lift_back():
    """Moves the back stepper upwards, from the base position"""
    motor.set_motor(STEP_BACK, 100)

def lower_both():
    lower_back()
    lower_front()

def lift_both():
    lift_back()
    lift_front()

if __name__ == '__main__':
    try:
        # lower_front()
        # lower_back()
        lift_back()

        input()
        stop()

        # forwards()
        time.sleep(10)
    finally:
        stop()
