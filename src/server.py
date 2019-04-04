#!/usr/bin/env python3
"""A basic server for the demo days."""

# pylint: disable=W0611

import asyncio
import inspect
import logging
import signal
import sys
import time
from typing import Any, Dict

import autonomous_control as control
import log
import motor
from data import SensorData
from i2c_sensor_thread import RotaryEncoderThread

NETWORK_LOG = logging.getLogger("Network")

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
    if loop.is_running():
        logging.error("Terminating loop due to error")
        loop.stop()
    loop.default_exception_handler(context)

async def motor_control(queue: SingleValueQueue, manager: ConnectionManager, data: SensorData) -> None:
    """Pulls events from `queue` and executes them on the motors"""
    motor.stop_motors()

    commands = control.__dict__
    motor_log = logging.getLogger("Motor")
    while True:
        action = (await queue.pull()).lower().replace(' ', '_')
        motor.stop_motors()
        await asyncio.sleep(0.005)

        if 'stop' in action:
            # Stop commands are executed as-is
            motor_log.info("Stopping")
            manager.send("Idle")
            data.set_moving(False)
            control.stop()
        elif action in commands:
            # If we're a function defined in the control module, execute it.
            data.set_moving(True)
            motor_log.info("Running %s", action)
            manager.send("Running " + action)
            command = commands[action]

            # Prepare call for this command
            params = inspect.signature(command).parameters
            args = {} # type: Dict[str, Any]
            if "data" in params:
                args["data"] = data
            if "callback" in params:
                args["callback"] = manager.send

            command(**args)
        else:
            manager.send("Doing goodness knows what.")

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

        NETWORK_LOG.info('Connection from %s', self.peername)
        self.manager.add(self)

    def connection_lost(self, exc):
        NETWORK_LOG.info('Lost connection from %s (%s)', self.peername, exc)
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

            NETWORK_LOG.debug('Message received: %s', message)
            self.queue.push(message)

    def send(self, message):
        """Send a `message` to the connected client."""
        self.transport.write((message + "\n").encode())

async def check_sensors(data: SensorData) -> None:
    """Monitors the two distance sensors for 2 seconds, and errors if they
       never produce any valid value

    """
    start = time.time()
    while time.time() - start < 2:
        if data.front_ground_touch.valid:
            return

        await asyncio.sleep(0.1)

    raise IOError("Sensor data is still invalid after 2 seconds.")

def cleanup() -> None:
    """Close all tasks currently running"""
    for task in asyncio.Task.all_tasks():
        task.cancel()

def _main():
    """The main entry point of the server"""

    log.configure()

    control.stop()

    # Create an event loop. This effectively allows us to run multiple functions
    # at once (namely, the motor controller and server).
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(exception_handler)

    # Motor control statements are pushed into this queue
    motor_queue = SingleValueQueue()

    # And we hold all currently connected computers here
    manager = ConnectionManager()

    # Grab our sensor data
    data = SensorData()

    if "-M" not in sys.argv:
        loop.create_task(motor_control(motor_queue, manager, data))

    # Create the sensor thread
    thread_i2c_sensors = RotaryEncoderThread(1, 5, data)
    thread_i2c_sensors.setDaemon(5)
    thread_i2c_sensors.start()

    # Construct the server and run it forever
    server = None
    try:
        with data.front_dist_0, \
             data.front_dist_1, \
             data.front_ground_dist, \
             data.back_ground_dist, \
             data.front_ground_touch, \
             data.middle_stair_touch, \
             data.back_stair_touch, \
             data.back_ground_touch, \
             data.middle_ground_touch:

            # Reset the front and back to clear any residual data
            server = loop.run_until_complete(loop.create_server(
                lambda: SpencerServerConnection(motor_queue, manager),
                '0.0.0.0', 1050
            ))

            NETWORK_LOG.info('Serving on %s', server.sockets[0].getsockname())

            # Wait for 2 seconds to ensure the server is ready
            loop.run_until_complete(check_sensors(data))

            # Zero the motors
            loop.run_until_complete(control.zero(data, manager.send))

            loop.run_forever()
    finally:
        if server is not None:
            server.close()
            loop.run_until_complete(server.wait_closed())

        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

        if "-M" not in sys.argv:
            motor.float_motors()

if __name__ == "__main__":
    _main()
