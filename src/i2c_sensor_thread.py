from threading import Thread
from data import SensorData as data
import time
import smbus2

class SensorsI2c(Thread):
    """ thread class for i2c sensors """

    def __init__(self, i2c_bus_no, address):
        self.address = address
        self.bus_no = i2c_bus_no
        self.bus = smbus2.SMBus(i2c_bus_no)
        self.bus.write_byte(address, 255)
        Thread.__init__(self)

    def run(self):
        while True:
            state = self.bus.read_byte(self.address)
            #TODO(anyone) Add touch sensors below call by using on change and passing the state
            data.middle_ground_touch.set(not bool(state & 0x1))
            data.back_stair_touch.set(not bool(state & 0x2))
            data.back_lifting_normal.set(not bool(state & 0x4))
            data.back_lifting_extended_max.set(not bool(state & 0x8))
            time.sleep(0.01)
