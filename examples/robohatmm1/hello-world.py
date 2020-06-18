# Write your code here :-)
import time
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while(True):
    led.value = True
    time.sleep(0.5)
    led.value = False
    print("Hello, World! This is CircuitPython")
    time.sleep(0.5)
