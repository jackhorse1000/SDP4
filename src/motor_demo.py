"""
A basic example of controlling a motor via smbus
"""

import time

import motor

try:
    # motor.set_motor(4, -100)
    # motor.set_motor(5, -100)
    # motor.set_motor(1, 100)
    # motor.set_motor(3, -100)

    while True:
        time.sleep(0.1)
finally:
    motor.stop_motors()
