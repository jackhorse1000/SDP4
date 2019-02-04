"""
A basic example of controlling a motor via smbus
"""

import time

import motor

def forward():
    """Move motors forwards."""
    motor.set_motor(4, 50)
    motor.set_motor(5, 50)

def lift_front_part():
    """Lift the front part"""
    motor.set_motor(3, 100)

def stop():
    """Stop all motors"""
    motor.stop_motors()

def _main():
    print("Caesar")
    motor.set_motor(2, 100)
    time.sleep(3)
    print("Caesar1")

    #lift_front_part()
    time.sleep(3)
    stop()
    exit()

if __name__ == "__main__":
    _main()

try:
    while True:
        #motor.set_motor(4, -100)
        #motor.set_motor(5, 100)
        motor.set_motor(1, 100)
        #time.sleep(3)
        #motor.stop_motors()
        #time.sleep(0.5)

        #motor.set_motor(4, 100)
        #motor.set_motor(5, -100)

        #time.sleep(3)
        #motor.stop_motors()
        #time.sleep(0.5)

    # motor.set_motor(1, 100)
    # motor.set_motor(3, -100)
finally:
    motor.stop_motors()
