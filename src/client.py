import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('129.215.33.139', 8081))
while True:
    data = s.recv(1)
    if data == "1":
        # Turn on motor
        pass
    else:
        # Turn off motor
        pass

    # I'm afraid the motor stuff is on the Pi, and I've forgotten quite
    # what it looked like.

s.close()
