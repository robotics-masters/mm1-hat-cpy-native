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
pwm1 = pulseio.PWMOut(board.SERVO2, duty_cycle=2 ** 15, frequency=50)
pwm2 = pulseio.PWMOut(board.SERVO3, duty_cycle=2 ** 15, frequency=50)
pwm3 = pulseio.PWMOut(board.SERVO4, duty_cycle=2 ** 15, frequency=50)
pwm4 = pulseio.PWMOut(board.SERVO5, duty_cycle=2 ** 15, frequency=50)
pwm5 = pulseio.PWMOut(board.SERVO7, duty_cycle=2 ** 15, frequency=50)

my_servo_0 = servo.Servo(pwm)
my_servo_1 = servo.Servo(pwm1)
my_servo_2= servo.Servo(pwm2)
my_servo_3 = servo.Servo(pwm3)
my_servo_4 = servo.Servo(pwm4)
my_servo_5 = servo.Servo(pwm5)



servos = [my_servo_0, my_servo_1, my_servo_2,
            my_servo_3, my_servo_4, my_servo_5]



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
        for my_servo in servos:
            my_servo.angle = angle
        time.sleep(0.05)
    for angle in range(180, 0, -5):
        for my_servo in servos:
            my_servo.angle = angle
        time.sleep(0.05)
    led.value = False
    time.sleep(0.5)
