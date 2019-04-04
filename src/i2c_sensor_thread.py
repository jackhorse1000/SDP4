"""Helper code for polling I2C touch sensors"""

from threading import Thread
import time

import smbus2

from data import SensorData

class RotaryEncoderThread(Thread):
    """Polls the rotary encoder and updates the relevant sensors."""
    def __init__(self, i2c_bus_no: int, address: int, data: SensorData) -> None:
        self.address = address
        self.bus = smbus2.SMBus(i2c_bus_no)
        self.data = data

        super().__init__()

    def run(self):
        while True:
            msg = smbus2.i2c_msg.read(5, 2)
            self.bus.i2c_rdwr(msg)
            for i, val in enumerate(msg):
                if val >= 128:
                    val = -256 + val

                if i == 1:
                    self.data.front_lifting_rot.change(val)
                elif i == 0:
                    self.data.back_lifting_rot.change(val)

            time.sleep(0.05)
