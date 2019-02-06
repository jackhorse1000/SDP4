"""Helper methods for interfacing with Phidget sensors."""

import asyncio
import logging

from Phidget22.Devices.VoltageRatioInput import VoltageRatioInput, VoltageRatioSensorType
from Phidget22.Devices.DigitalInput import DigitalInput


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
        self.valid = False
        self.loop = asyncio.get_event_loop()

        self.phidget = VoltageRatioInput()
        self.phidget.setChannel(channel)
        self.phidget.setOnSensorChangeHandler(self.on_change)
        self.phidget.setOnErrorHandler(self.on_error)

    def attach(self):
        """Attach this sensor and configure it with various properties.

           For now, we update the input when we receive a change <= 0.005, which
           translates to a pretty small distance change (~.02cm).

        """
        self.phidget.openWaitForAttachment(ATTACHEMENT_TIMEOUT)
        self.phidget.setVoltageRatioChangeTrigger(0.005)
        self.phidget.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1101_SHARP_2D120X)

    def _on_change(self, _, value, unit):
        "Callback for when the sensor's input is changed."""
        LOG.debug("%s = %s%s", self.name, value, unit.symbol)

        # Update properties and notify observers
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
            if self.valid:
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
    tasks = { asyncio.get_event_loop().create_task(sensor.get()) for sensor in sensors }
    done, pending = await asyncio.wait(tasks, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
    for pend in pending:
        pend.cancel()
    return


if __name__ == '__main__':
    import log, time, math
    log.configure()

    loop = asyncio.get_event_loop()
    try:
        with Distance("Left", 0) as left, Distance("Right", 1) as right:
            left.attach()
            right.attach()

            async def main():
                while True:
                    await wait_input(left, right)

                    if left.valid and right.valid:
                        delta = left.value - right.value
                        if abs(delta) <= 0.05:
                            logging.info("Roughly level (%f)", delta)
                        else:
                            logging.info("Angle = %f (%fcm, %fcm)", 90 - math.degrees(math.atan2(6.5, delta)), left.value, right.value)

            loop.run_until_complete(main())
    finally:
        loop.close()
