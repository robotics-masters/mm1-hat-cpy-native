#RPi Power Test.
#This is the circuitpython code for it, but I haven't tested.

import board
from digitalio import DigitalInOut, Direction, Pull

off_pin = DigitalInOut(board.POWER_OFF)
off_pin.direction = Direction.OUTPUT

on_pin = DigitalInOut(board.POWER_ON)
on_pin.direction = Direction.OUTPUT

# turn the board off
off_pin.value = True
on_pin.value = not off_pin.value

# turn the board on
off_pin.value = False
on_pin.value = not off_pin.value

