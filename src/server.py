"""A basic server for the demo days"""

import asyncio

async def wakeup():
    """A really ugly hack to allow throwing interrupts within the event loop"""
    while True:
        await asyncio.sleep(0.1)

class SpencerServerProtocol(asyncio.Protocol):
    """The main protocol for Spencer"""

    def __init__(self):
        self.peername = None
        self.transport = None
        self.buffer = ""
        self.count = 0

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(self.peername))
        self.transport = transport

        self.send('Doing nothing')

    def connection_lost(self, exc):
        print('Lost connection from {} ({})'.format(self.peername, exc))

    def data_received(self, data):
        print('Data received')

        messages = (self.buffer + data.decode()).split("\n")
        self.buffer = messages.pop()

        for message in messages:
            self.count += 1
            print('Message received: {}'.format(message))
            self.send("Received {} messages".format(self.count))

    def send(self, message):
        """Send message to the server"""
        self.transport.write((message + "\n").encode())

def _main():
    loop = asyncio.get_event_loop()
    loop.create_task(wakeup())

    # Construct the server
    server = loop.run_until_complete(loop.create_server(SpencerServerProtocol, '0.0.0.0', 1050))

    print('Serving on {}'.format(server.sockets[0].getsockname()))

    # And run it forever
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

if __name__ == "__main__":
    _main()
