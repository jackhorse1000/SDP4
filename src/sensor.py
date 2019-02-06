"""Helper methods for interfacing with Phidget sensors."""

import asyncio
import logging

from Phidget22.Devices.VoltageRatioInput import VoltageRatioInput, VoltageRatioSensorType
from Phidget22.Devices.DigitalInput import DigitalInput
from Phidget22.Devices.Log import Log, LogLevel


LOG = logging.getLogger("Sensors")

ATTACHEMENT_TIMEOUT = 1000

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

class Distance:
    """A glorified wrapper over the distance sensor."""
    def __init__(self, name, channel):
        self.name = name
        self.event = asyncio.Event()
        self.value = 0
        self.valid = None
        self.loop = asyncio.get_event_loop()

        self.phidget = VoltageRatioInput()
        self.phidget.setChannel(channel)
        self.phidget.setOnSensorChangeHandler(self._on_change)
        self.phidget.setOnErrorHandler(self._on_error)

    def attach(self):
        """Attach this sensor and configure it with various properties.

           For now, we subscribe to updatees every 50ms (20Hz). However,
           we only fire off the event listeners if this results in a
           change of 5mm, to avoid too much noise.

        """
        self.phidget.openWaitForAttachment(ATTACHEMENT_TIMEOUT)
        self.phidget.setDataInterval(50)
        self.phidget.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1101_SHARP_2D120X)
        LOG.debug("Attached %s", self.name)

    def _on_change(self, _, value, unit):
        "Callback for when the sensor's input is changed."""
        if not self.valid or abs(self.value - value) > 0.05:
            # Update properties and notify observers
            LOG.debug("%s = %s%s", self.name, value, unit.symbol)

            self.value = value
            self.valid = True
            self.loop.call_soon_threadsafe(self.event.set)

    def _on_error(self, ph, code, msg):
        """Callback for when the sensor detects receives an error.

           We have a special implementation, as we want to handle the case where
           the input is out of range.

        """
        if code == 4103:
            # Mark as malfrormed and notify observers
            if self.valid != True:
                LOG.warning("%s is out of bounds", self.name)
                self.valid = False
                self.loop.call_soon_threadsafe(self.event.set)
        else:
            on_error(ph, code, msg)

    def __enter__(self):
        return self

    def __exit__(self, _a, _b, _c):
        self.phidget.setOnErrorHandler(None)
        self.phidget.setOnSensorChangeHandler(None)
        self.phidget.close()

    async def wait(self):
        """Wait for this sensor to receive new input."""
        await self.event.wait()
        self.event.clear()

async def wait_input(*sensors, timeout=None):
    """Wait for input from one or more of the given sensors."""
    tasks = { asyncio.get_event_loop().create_task(sensor.wait()) for sensor in sensors }
    done, pending = await asyncio.wait(tasks, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
    for pend in pending:
        pend.cancel()
    return len(done) > 0

if __name__ == '__main__':
    import log, time, math, control
    log.configure()
    Log.enable(LogLevel.PHIDGET_LOG_VERBOSE, "phidget.log")

    loop = asyncio.get_event_loop()
    try:
        with Distance("Left", 0) as left, Distance("Right", 1) as right:
            left.attach()
            right.attach()

            async def main():
                while True:
                    ok = await wait_input(left, right , timeout=3)

                    if ok and left.valid and right.valid:
                        distance = min(left.value, right.value)
                        delta = left.value - right.value
                        logging.debug("Distance=%f, delta of %f", distance, delta)

                        if distance >= 10:
                            control.forward()
                        elif distance < 6:
                            control.backward()
                        elif delta > 0.5:
                            control.turn_right()
                        elif delta < -0.5:
                            control.turn_left()
                        else:
                            control.stop()
                    else:
                        control.stop()

            loop.run_until_complete(main())
    finally:
        loop.close()
        control.stop()
