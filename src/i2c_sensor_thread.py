"""Helper code for polling I2C touch sensors"""

from threading import Thread
import time

import smbus2

from data import SensorData

class SensorsI2c(Thread):
    """ thread class for i2c sensors """

    def __init__(self, i2c_bus_no, address, data: SensorData) -> None:
        self.address = address
        self.bus_no = i2c_bus_no
        self.bus = smbus2.SMBus(i2c_bus_no)
        self.bus.write_byte(address, 255)
        self.data = data

        super().__init__()

    def run(self):
        while True:
            state = self.bus.read_byte(self.address)
            #TODO(anyone) Add touch sensors below call by using on change and passing the state
            self.data.middle_ground_touch.set(not bool(state & 0x1))
            self.data.back_stair_touch.set(not bool(state & 0x2))
            self.data.back_lifting_normal.set(not bool(state & 0x4))
            self.data.back_lifting_extended_max.set(not bool(state & 0x8))
            time.sleep(0.01)
