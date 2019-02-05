"""Helper methods for interfacing with Phidget sensors."""

import logging

LOG = logging.getLogger("Sensors")

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
