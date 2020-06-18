# CircuitPython demo - NeoPixel
from time import sleep
import board
import neopixel
 
pixel_pin = board.NEOPIXEL
num_pixels = 375
 
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)
 
def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        sleep(wait)
        pixels.show()
    sleep(0.5)
 
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
 
while True:
    pixels.fill(RED)
    pixels.show()
    # Increase or decrease to change the speed of the solid color change.
    sleep(1)
    pixels.fill(GREEN)
    pixels.show()
    sleep(1)
    pixels.fill(BLUE)
    pixels.show()
    sleep(1)
 
    color_chase(RED, 0.1)
    color_chase(YELLOW, 0.1)
    color_chase(GREEN, 0.1)
