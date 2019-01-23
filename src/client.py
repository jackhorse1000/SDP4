import socket, smbus
import numpy as np

bus = smbus.SMBus(1)
address = 0x04

def write_bus(value):
    bus.write_byte_data(address, 0x00, value)

def setMotor( id, speed):
    """
    Mode 2 is Forward.
    Mode 3 is Backwards.
    """
    direction = 2 if speed >= 0 else 3
    speed = np.clip(abs(speed), 0, 100)
    byte1 = id << 5 | 24 | direction << 1
    byte2 = int(speed * 2.55)
    write_bus(byte1)
    write_bus(byte2)

def stopMotor(id):
    """
    Mode 0 floats the motor.
    """
    direction = 0
    byte1 = id << 5 | 16 | direction << 1
    write_bus(byte1)

def stopMotors():
    """
    The motor board stops all motors if bit 0 is high.
    """
    print('[INFO] [MotorControl] Stopping all motors...')
    write_bus(0x01)

# @asyncio.coroutine
# def tcp_echo_client(message, loop):
#     reader, writer = yield from asyncio.open_connection('joncoates.co.uk', 8082, loop=loop)

#     print('Send: %r' % message)
#     writer.write(message.encode())

#     while True:
#         data = yield from reader.read(100)
#         print('Received: %r' % data.decode())

#     print('Close the socket')
#     writer.close()

# message = 'Hello World!'
# loop = asyncio.get_event_loop()
# loop.run_until_complete(tcp_echo_client(message, loop))
# loop.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('129.215.33.139', 8081))

try:
    while True:
        data = s.recv(100)
        if data == '1':
            setMotor(5, 30)
        else:
            stopMotor(5)
        print(data, type(data))
finally:
    s.close()
    stopMotors()
