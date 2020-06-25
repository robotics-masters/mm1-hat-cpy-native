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
first_press = 0

while True:
    if pressed == False:
        pressed = button.value
        first_press = time.monotonic()

    if button.value == False and pressed and (first_press + TIME_BETWEEN_PRESS < time.monotonic()):
        print("single press")
        pressed = False
    elif button.value and pressed and (first_press + TIME_BETWEEN_PRESS < time.monotonic()):
        print("long press")
        pressed = False
        while button.value:
            continue
        
    led.value = button.value
    time.sleep(0.1)
