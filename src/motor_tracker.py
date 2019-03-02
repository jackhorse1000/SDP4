import smbus2
import motor
import autonomous_control as control
import time
from threading import Thread

motors = [0] * 6

BUS = smbus2.SMBus(1)
class UpdateMotors(Thread):
    def run(self):
        while True:
            BUS.write_byte(5, 6)
            for i in range(6):
                val = BUS.read_byte(5)
                if val >= 128:
                    val = -256 + val
                motors[i] += val

            print(motors)

            # We need this delay in order to prevent flooding serial out. Whether it needs to be
            # this high is a whole nother kettle of fish.
            time.sleep(0.05)

if __name__ == "__main__":
    t = UpdateMotors()
    # t.setDaemon(True)
    t.start()

    try:
        control.lift_front()
        time.sleep(1.5)

        while abs(motors[0]) > 20:
            count = 0
            while count < 10:
                time.sleep(0.05)

                if abs(motors[0]) <= 40:
                    control.stop()
                    count += 1
                    continue

                count = 0
                if motors[0] > 0:
                    control.lift_front()
                else:
                    control.lower_front()


    finally:
        control.stop()
