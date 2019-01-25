"""
A basic example of controlling a motor via smbus
"""

import smbus2

BUS = smbus2.SMBus(1)
ADDRESS = 0x04

def _write_bus(value):
    BUS.write_byte_data(ADDRESS, 0x00, value)

def set_motor(motor_id, speed):
    """Sets a motor at a specific speed"""

    # Mode 2 is Forward.
    # Mode 3 is Backwards.
    direction = 2 if speed >= 0 else 3
    speed = max(0, min(100, abs(speed)))
    byte1 = motor_id << 5 | 24 | direction << 1
    byte2 = int(speed * 2.55)
    _write_bus(byte1)
    _write_bus(byte2)

def stop_motor(motor_id):
    """Stops the given motor"""
    # Mode 0 floats the motor.
    direction = 0
    byte1 = motor_id << 5 | 16 | direction << 1
    _write_bus(byte1)

def stop_motors():
    """Stops all motors"""
    # The motor board stops all motors if bit 0 is high.
    _write_bus(0x01)
