# CircuitPython Test for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython 3.1
#
import board
import digitalio
import time
import pulseio
from adafruit_motor import servo

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


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
