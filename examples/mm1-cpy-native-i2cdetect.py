# CircuitPython Test for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython 3.1
#
import board
import digitalio
import time
import busio


# set up the signal and servo pins
signal_pins = [board.SIGNAL1, board.SIGNAL2, board.SIGNAL3,
               board.SIGNAL4, board.SIGNAL5, board.SIGNAL6,
               board.SIGNAL7, board.SIGNAL8, board.SIGNAL9,
               board.SIGNAL10, board.SIGNAL11]

servo_pins = [board.SERVO1, board.SERVO2, board.SERVO3,
              board.SERVO4, board.SERVO5, board.SERVO6,
              board.SERVO7, board.SERVO8]

rc_pins = [board.RCH1, board.RCH2, board.RCH3, board.RCH4]

signals = []
servos = []
rchs = []

# setup I2C
i2c = busio.I2C(board.SCL, board.SDA)



# TESTS
#  This runs in the following order:
#   1. i2c scan
#   2. sleep for 3 seconds
#

while True:
    while not i2c.try_lock():
        pass

    [hex(x) for x in i2c.scan()]

    i2c.unlock()

    time.sleep(3)

