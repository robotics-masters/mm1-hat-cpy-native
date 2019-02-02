# CircuitPython Test for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython 3.1
#
import board
import digitalio
import time

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

# set up
for pin in signal_pins:
    signals.append(digitalio.DigitalInOut(pin))

for pin in servo_pins:
    servos.append(digitalio.DigitalInOut(pin))

for pin in rc_pins:
    rchs.append(digitalio.DigitalInOut(pin))

# set as output
for pin in signals:
    pin.direction = digitalio.Direction.OUTPUT

for pin in servos:
    pin.direction = digitalio.Direction.OUTPUT

for pin in rchs:
    pin.direction = digitalio.Direction.OUTPUT


# TESTS
#  This runs in the following order:
#   1. Servos
#   2. Radio Channels
#   3. Signals
#
# Each test turns the pin on for 0.5 seconds then off.
# Then the test repeats.

## test servos

while True:
    for pin in servos:
        pin.value = True
        time.sleep(0.5)
        pin.value = False
        time.sleep(0.5)

    for pin in rchs:
        pin.value = True
        time.sleep(0.5)
        pin.value = False
        time.sleep(0.5)

    for pin in signals:
        pin.value = True
        time.sleep(0.5)
        pin.value = False
        time.sleep(0.5)

