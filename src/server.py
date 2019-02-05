"""A basic server for the demo days."""

import asyncio
import sys

from Phidget22.Devices.VoltageRatioInput import VoltageRatioInput, VoltageRatioSensorType
from Phidget22.Devices.DigitalInput import DigitalInput
from Phidget22.Phidget import ChannelSubclass

import control
import motor

class ConnectionManager:
    """Manages a set of connections, with the ability to send messages to all
       connected clients.

    """
    def __init__(self):
        self.connections = set()

    def add(self, connection):
        """Add a connection to the manager"""
        self.connections.add(connection)

    def remove(self, connection):
        """Remove a connection from the manager"""
        self.connections.remove(connection)

    def send(self, message):
        """Send a message to all current connections"""
        message = (message + "\n").encode()
        for connection in self.connections:
            connection.transport.write(message)

class SingleValueQueue:
    """An asyncronous queue which holds a single value. Simply used to push values
       between the connections and the motor controller.

    """
    def __init__(self):
        self.value = None
        self.event = asyncio.Event()

    async def pull(self):
        """Wait for an event to be available and pull it."""
        await self.event.wait()
        self.event.clear()
        return self.value


    def push(self, value):
        """Push an event to the queue. This will either overwrite the existing event or
           notify the listening client with it.

        """
        self.value = value
        self.event.set()

def exception_handler(loop, context):
    """A custom error handler for the loop, which stops the loop before continuing to
       the default handler

    """
    print("\33[1;31mTerminating loop due to error\33[0m")
    if loop.is_running():
        loop.stop()
    loop.default_exception_handler(context)

async def wakeup():
    """A really ugly hack to ensure interrupts are thrown within the event loop.

    """
    while True:
        await asyncio.sleep(0.1)

async def motor_control(queue, manager):
    """Pulls events from `queue` and executes them on the motors"""
    motor.stop_motors()

    commands = control.__dict__
    while True:
        action = (await queue.pull()).lower().replace(' ', '_')
        motor.stop_motors()
        await asyncio.sleep(0.005)

        if 'stop' in action:
            # Stop commands are executed as-is
            manager.send("Idle")
            control.stop()
        elif action in commands:
            # If we're a function defined in the control module, execute it.
            manager.send("Running " + action)
            commands[action]()
        else:
            manager.send("Doing goodness knows what.")


def sensor_setup(ph):
    """When a sensor is attached, we configure it with various properties (interval between receiving inputs,
       minimum change required before we get an input, etc...)

    """
    ph.setDataInterval(100)
    ph.setVoltageRatioChangeTrigger(0.0)
    if ph.getChannelSubclass() == ChannelSubclass.PHIDCHSUBCLASS_VOLTAGERATIOINPUT_SENSOR_PORT:
        ph.setVoltageRatioChangeTrigger(0.005)
        ph.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_VOLTAGERATIO)

def sensor_error(_ph, code, string):
    """We get error messages if the sensor receives values outside its operating parameters."""
    sys.stderr.write("[Phidget Error Event] -> " + string + " (" + str(code) + ")\n")

def sensor_change(manager):
    """The above event is processed by the Phidget API and converted into a distance."""
    def handler(_ph, value, unit):
        print("Sensor %s%s" % (value, unit.symbol))
        manager.send("sensor %s%s" % (value, unit.symbol))
    return handler

def digital_change(manager):
    """The above event is processed by the Phidget API."""
    def handler(_ph, value):
        print("Sensor %s" % (value))
        manager.send("sensor %s" % (value))
    return handler

class SpencerServerConnection(asyncio.Protocol):
    """Represents a socket connection to a "spencer client". Namely, a phone running
       the spencer app.

       This simply registers itself in the connection manager, and assumes all
       incomming messages are motor controls.

    """

    def __init__(self, queue, manager):
        self.queue = queue
        self.manager = manager

        self.peername = None
        self.transport = None
        self.buffer = ""
        self.count = 0

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        self.transport = transport

        print('Connection from {}'.format(self.peername))
        self.manager.add(self)

    def connection_lost(self, exc):
        print('Lost connection from {} ({})'.format(self.peername, exc))
        self.manager.remove(self)
        self.queue.push("stop")

    def data_received(self, data):
        # Messages are terminated by a new line, so add to our existing buffer
        # an split on \n. Any non-terminated data will be stored back in
        # `self.buffer` again.
        messages = (self.buffer + data.decode()).split("\n")
        self.buffer = messages.pop()
        # I'm going to confess, the above code is horrible. It works though!

        for message in messages:
            self.count += 1

            # Delete trailing \r if we're commanding it via telnet (goodness, I
            # hope not)
            if message.endswith("\r"):
                message = message[:-1]

            print('Message received: {}'.format(message))
            self.queue.push(message)

    def send(self, message):
        """Send a `message` to the connected client."""
        self.transport.write((message + "\n").encode())

def _main():
    """The main entry point of the server"""

    # Create an event loop. This effectively allows us to run multiple functions
    # at once (namely, the motor controller and server).
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(exception_handler)
    # Motor control statements are pushed into this queue
    motor_queue = SingleValueQueue()
    # And we hold all currently connected computers here
    manager = ConnectionManager()

    # Create our voltage channel
    channel = VoltageRatioInput()
    channel.setChannel(0)
    channel.setOnAttachHandler(sensor_setup)
    channel.setOnErrorHandler(sensor_error)
    channel.setOnSensorChangeHandler(sensor_change(manager))

    # Create our sensor channel
    sensor_channel_0 = DigitalInput()
    sensor_channel_0.setChannel(0)
    # sensor_channel_0.setOnAttachHandler(sensor_setup)
    sensor_channel_0.setOnErrorHandler(sensor_error)
    sensor_channel_0.setOnStateChangeHandler(digital_change(manager))

    # Create our sensor channel
    sensor_channel_1 = DigitalInput()
    sensor_channel_1.setChannel(1)
    # sensor_channel_1.setOnAttachHandler(sensor_setup)
    sensor_channel_1.setOnErrorHandler(sensor_error)
    sensor_channel_1.setOnStateChangeHandler(digital_change(manager))


    # Register our tasks which run along side the server
    loop.create_task(wakeup())
    loop.create_task(motor_control(motor_queue, manager))

    # Construct the server and run it forever
    server = None
    try:
        # Wait for attachement and set the sensor type to the 10-80cm distance one
        if "-P" not in sys.argv:
            channel.openWaitForAttachment(1000)
            sensor_channel_0.openWaitForAttachment(1000)
            sensor_channel_1.openWaitForAttachment(1000)
            channel.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1101_SHARP_2Y0A21)

        server = loop.run_until_complete(loop.create_server(
            lambda: SpencerServerConnection(motor_queue, manager),
            '0.0.0.0', 1050
        ))

        print('Serving on {}'.format(server.sockets[0].getsockname()))

        loop.run_forever()
    finally:
        if server is not None:
            server.close()
            loop.run_until_complete(server.wait_closed())

        loop.close()

        channel.setOnVoltageRatioChangeHandler(None)
        channel.setOnSensorChangeHandler(None)
        sensor_channel_0.setOnStateChangeHandler(None)
        sensor_channel_1.setOnStateChangeHandler(None)
        channel.close()

        motor.stop_motors()

if __name__ == "__main__":
    _main()
