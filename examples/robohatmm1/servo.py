import board
import digitalio
import time
import pulseio
from adafruit_motor import servo

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# set up
pwm = pulseio.PWMOut(board.SERVO1, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)



# TESTS
#  This runs in the following order:
#   1. Single Servo
#
# Then the test repeats.

## test servo

while True:
    led.value = True
    time.sleep(0.5)
    for angle in range(0, 180, 5):
        my_servo.angle = angle
        time.sleep(0.05)
    for angle in range(180, 0, -5):
        my_servo.angle = angle
        time.sleep(0.05)
    led.value = False
    time.sleep(0.5)
