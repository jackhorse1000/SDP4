"""Helper methods for interfacing with Phidget sensors."""

import logging
import threading
from typing import Optional
import time


from Phidget22.Devices.VoltageRatioInput import VoltageRatioInput, VoltageRatioSensorType
from Phidget22.Devices.DigitalInput import DigitalInput

LOG = logging.getLogger("Sensors")

ATTACHMENT_TIMEOUT = 1000

def current_milli_time() -> int:
    """Get the current time in milliseconds"""
    return int(round(time.time() * 1000))

def on_error(ph, code, msg):
    """We get error messages if the sensor receives values outside its operating parameters."""
    LOG.error("%s %d: %s (%d)", ph.getChannelClassName(), ph.getChannel(), msg, code)

def setup(factory, channel):
    """Setup a new sensor using the given factory type and channel.

       This simply acts as a little helper method to make registration code
       shorter.

    """
    ph = factory()
    ph.setChannel(channel)
    ph.setOnErrorHandler(on_error)
    return ph

class Touch:
    """A glorified wrapper over the touch sensor."""
    name = None # type: str
    value = None # type: int
    valid = None # type: bool

    def __init__(self, name: str, channel: int):
        self.name = name
        self.value = 0
        self.valid = False

        self.lock = threading.Lock()

        self.phidget = DigitalInput()
        self.phidget.setChannel(channel)
        self.phidget.setOnStateChangeHandler(self._on_change)

        # TODO(anyone): Look into this
        self.phidget.setOnErrorHandler(on_error)

    def _on_change(self, _, state):
        "Callback for when the sensor's input is changed."""
        LOG.debug("%s = %s", self.name, state)
        with self.lock:
            self.valid = True
            self.value = state

    def get(self) -> bool:
        """ Returns the value of the sensors data """
        with self.lock:
            data = self.value
        return data == 1

    def set(self, value):
        """ Sets the value of the sensors data """
        if self.value != value:
            LOG.debug("%s = %s", self.name, value)
        with self.lock:
            self.valid = True
            self.value = value

    def __enter__(self):
        """Attach this sensor and configure it with various properties.

        """
        self.phidget.openWaitForAttachment(ATTACHMENT_TIMEOUT)
        LOG.info("Attached %s", self.name)

    def __exit__(self, _a, _b, _c):
        self.phidget.setOnErrorHandler(None)
        self.phidget.setOnStateChangeHandler(None)
        self.phidget.close()

class TouchSensorsI2c:
    """A touch sensor from the I2C expansion board."""

    name = None # type: str
    value = None # type: bool
    prev_value = None # type: bool
    time = None # type: int

    """ touch sensors connected to the i2c """
    def __init__(self, name: str) -> None:
        """ init for i2c bus """
        self.name = name
        self.lock = threading.Lock()
        self.value = False
        self.prev_value = False
        self.time = 0

    def get(self)-> bool:
        """ Returns the value of the pin """
        with self.lock:
            if current_milli_time() - self.time > 100:
                data = self.value
            else:
                data = self.prev_value
        return data

    def set(self, value: bool) -> None:
        """ Sets the value of the sensors data """
        with self.lock:
            if self.value != value:
                self.time = current_milli_time()
                self.prev_value = self.value
                self.value = value
                LOG.debug("%s = %s", self.name, value)


class Distance:
    """A glorified wrapper over the distance sensor."""

    name = None # type: str
    value = None # type: float
    valid = None # type: Optional[bool]

    def __init__(self, name: str, channel: int):
        self.name = name
        self.value = 0
        self.valid = None

        self.lock = threading.Lock()

        self.phidget = VoltageRatioInput()
        self.phidget.setChannel(channel)
        self.phidget.setOnSensorChangeHandler(self._on_change)
        self.phidget.setOnErrorHandler(self._on_error)

    def _on_change(self, _, value, _unit):
        "Callback for when the sensor's input is changed."""
        with self.lock:
            if not self.valid or abs(self.value - value) > 0.05:
                # Update properties and notify observers
                if self.name == "front_dist_0" or self.name == "front_dist_1":
                    LOG.debug("%s = %s%s", self.name, value, _unit.symbol)
                self.value = value
                self.valid = True

    def get(self) -> float:
        """ Returns the value of the sensors data """
        with self.lock:
            data = self.value
        return data

    def get_valid(self) -> Optional[bool]:
        """ Returns the true/false if the sensor reading is valid"""
        with self.lock:
            return self.valid

    def _on_error(self, ph, code, msg):
        """Callback for when the sensor detects receives an error.

           We have a special implementation, as we want to handle the case where
           the input is out of range.

        """
        if code == 4103:
            # Mark as malformed and notify observers
            with self.lock:
                if self.valid or self.valid is None:
                    LOG.warning("%s is out of bounds", self.name)
                    self.valid = False
        else:
            on_error(ph, code, msg)

    def __enter__(self):
        """Attach this sensor and configure it with various properties.

           For now, we subscribe to updates every 50ms (20Hz).
        """
        self.phidget.openWaitForAttachment(ATTACHMENT_TIMEOUT)
        self.phidget.setDataInterval(50)
        self.phidget.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1101_SHARP_2D120X)
        LOG.info("Attached %s", self.name)

        return self

    def __exit__(self, _a, _b, _c):
        self.phidget.setOnErrorHandler(None)
        self.phidget.setOnSensorChangeHandler(None)
        self.phidget.close()

class RotaryEncoder:
    """A rotary encoder sensor"""

    name = None # type: str
    value = None # type: int
    lock = None # type: threading.Lock

    def __init__(self, name: str) -> None:
        self.name = name
        self.value = 0
        self.lock = threading.Lock()

    def get(self) -> int:
        """Get the current value of this rotary encoder."""
        with self.lock:
            return self.value

    def change(self, delta: int) -> None:
        """Increment the encoder's value"""
        if delta != 0:
            with self.lock:
                self.value += delta
                LOG.debug("%s = %d", self.name, self.value)

    def reset(self) -> None:
        """Reset  the encoder's value to 0."""
        with self.lock:
            self.value = 0
            LOG.info("%s = %d (reset)", self.name, self.value)

class FakeSensor:
    """ Used to fake the sensors around the robot """

    def __init__(self, name: str):
        self.name = name
        self.value = 0
        self.lock = threading.Lock()

    def get(self):
        """ Returns the value of the sensors data """
        with self.lock:
            data = self.value
        return data

    def set(self, value):
        """ Set the value of the sensors data """
        with self.lock:
            self.value = value

    def __enter__(self):
        return self

    def __exit__(self, _a, _b, _c):
        return
