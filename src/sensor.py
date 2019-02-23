"""Helper methods for interfacing with Phidget sensors."""

import logging
import threading
from typing import Optional

from Phidget22.Devices.VoltageRatioInput import VoltageRatioInput, VoltageRatioSensorType
from Phidget22.Devices.DigitalInput import DigitalInput

LOG = logging.getLogger("Sensors")

ATTACHMENT_TIMEOUT = 1000

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
    # name: str
    # value: int
    # valid: bool

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
            self.value = state

    def get(self) -> bool:
        """ Returns the value of the sensors data """
        with self.lock:
            data = self.value
        return data == 1

    def __enter__(self):
        """Attach this sensor and configure it with various properties.

        """
        self.phidget.openWaitForAttachment(ATTACHMENT_TIMEOUT)
        LOG.debug("Attached %s", self.name)

    def __exit__(self, _a, _b, _c):
        self.phidget.setOnErrorHandler(None)
        self.phidget.setOnStateChangeHandler(None)
        self.phidget.close()

class Distance:
    """A glorified wrapper over the distance sensor."""

    # name: str
    # value: float
    # valid: Optional[bool]

    def __init__(self, name: str, channel: int):
        self.name = name
        self.value = 0
        self.valid = None

        self.lock = threading.Lock()

        self.phidget = VoltageRatioInput()
        self.phidget.setChannel(channel)
        self.phidget.setOnSensorChangeHandler(self._on_change)
        self.phidget.setOnErrorHandler(self._on_error)

    def _on_change(self, _, value, unit):
        "Callback for when the sensor's input is changed."""
        with self.lock:
            if not self.valid or abs(self.value - value) > 0.05:
                # Update properties and notify observers
                LOG.debug("%s = %s%s", self.name, value, unit.symbol)
                self.value = value
                self.valid = True

    def get(self) -> float:
        """ Returns the value of the sensors data """
        with self.lock:
            data = self.value
        return data

    def get_valid(self) -> bool:
        """ Returns the true/false if the sensor reading is valid"""
        with self.lock:
            is_valid = self.valid
        return is_valid

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
        LOG.debug("Attached %s", self.name)

        return self

    def __exit__(self, _a, _b, _c):
        self.phidget.setOnErrorHandler(None)
        self.phidget.setOnSensorChangeHandler(None)
        self.phidget.close()

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
