# CircuitPython Test for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython 3.1
#


import board
import digitalio
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.SIGNAL2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


while True:
    led.value = not button.value
    #led.value = True
    #time.sleep(0.5)
    #led.value = False
    time.sleep(0.01)
