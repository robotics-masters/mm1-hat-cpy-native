import board
import digitalio
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.BUTTON)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


while True:
    led.value = not button.value
    time.sleep(0.01)
