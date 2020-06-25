import board
import digitalio
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.BUTTON)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN

TIME_BETWEEN_PRESS = 0.5
pressed = False
first_press = time.monotonic()

while True:
    if pressed == False:
        pressed = button.value
        first_press = time.monotonic()

    if pressed and (first_press + TIME_BETWEEN_PRESS > time.monotonic()):
        

    
    #led.value = button.value
    time.sleep(0.1)
