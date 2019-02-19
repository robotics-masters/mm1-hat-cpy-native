# CircuitPython Test for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython 3.1
#
import time
import board

from analogio import AnalogIn
from digitalio import DigitalInOut, Direction

from pulseio import PWMOut
from adafruit_motor import servo

# set up on-board LED
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT


# set up servos and radio control channels

pwm1 = PWMOut(board.SERVO1, duty_cycle=2 ** 15, frequency=50)
pwm2 = PWMOut(board.SERVO2, duty_cycle=2 ** 15, frequency=50)
steering_servo = servo.Servo(pwm1)
throttle_servo = servo.Servo(pwm2)

steering_channel = AnalogIn(board.RCH1)
throttle_channel = AnalogIn(board.RCH2)


# functions
def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def get_angle(pin):
    return (180 * pin.value) / 65536

# TESTS
#  This runs in the following order:
#   1. Get value from both RCH
#   2. Send to respective servos
#   3. Send to Raspberry Pi (if connected)
#
# Then the test repeats.


## go-loop

while True:
    # get radio channel values
    #steering_servo.angle = get_angle(steering_channel)
    #throttle_servo.angle = get_angle(throttle_channel)
    print("Steering Angle: ", get_angle(steering_channel))

##    led.value = True
##    time.sleep(0.5)
##    for angle in range(0, 180, 5):
##        my_servo.angle = angle
##        time.sleep(0.05)
##    for angle in range(180, 0, -5):
##        my_servo.angle = angle
##        time.sleep(0.05)
##    led.value = False
##    time.sleep(0.5)
