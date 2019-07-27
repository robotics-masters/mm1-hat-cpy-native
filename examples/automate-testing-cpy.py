# CircuitPython Test for Robotics Masters Robo HAT MM1
#
# Notes:
#   This is to be run using CircuitPython 4.1
#
#
#   Date:  11-07-2019 1:05 PM
#  

import board
from digitalio import DigitalInOut, Direction
from pulseio import PWMOut
from adafruit_motor import servo
from busio import I2C
from time import sleep


##
##  This is a testing script for testing all functionality of
##   the Robo HAT MM1.  Follow the on-screen instructions to
##   test outputs and components.
##

### LED Test
print("[INFO] START - LED Test")

# setup LED
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

print("LED has been initialised.  It will flash FIVE times over a 10 second period.  Starting immediately.")

sleep(1)

# test LED
num_tests = 5
while (num_tests > 0):
    led.value = True
    sleep(1)
    led.value = False
    sleep(1)
    num_tests = num_tests - 1

print("[INFO] END - LED Test")


### i2c Test
print("[INFO] BEGIN - I2C Tests")

# setup i2c
i2c = I2C(board.SCL, board.SDA)

print("A list of all connected I2C devices will appear below.  This test will run THREE times.")

# test i2c (3 passes)
index = 3
while (index > 0):
    while not i2c.try_lock():
        pass

    [print(hex(x)) for x in i2c.scan()]

    i2c.unlock()

    sleep(3)
    index = index - 1

print("[INFO] END - I2C Test")

### SERVO Test
print("[INFO] START - SERVO Test")

print("Initialising all servo Pins.  There could be errors at this stage relating to timers.  Swap pins to remove errors and note in documentation.")

pins = [board.SERVO1, board.SERVO2, board.SERVO3, board.SERVO4,
        board.SERVO5, board.SERVO6, board.SERVO7, board.SERVO8]
servos = []

# set up servos
for pin in pins:
    print("[LOOP] Initialising...{0}".format(pin))
    pwm = PWMOut(pin, duty_cycle=2 ** 15, frequency=50)
    servos.append(servo.Servo(pwm))

print("[INFO] Finished setting up all servo pins, without issue.")

print("Now we will test each servo pin.  Attach a servo to SERVO1 for the first test.  As prompted each time, move the servo to the next pin for each test.")
print("The servo will sweep all the way to one end, and then back.  At which time, the test will be over and you must move the servo to the next pin.")

print("Testing will begin in 5 seconds.")
sleep(6)

for servo in servos:
    for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
        servo.angle = angle
        sleep(0.05)
    for angle in range(180, 0, -5): # 180 - 0 degrees, 5 degrees at a time.
        servo.angle = angle
        sleep(0.05)

    print("[INFO] - waiting 8 seconds")
    print("[WARN] == connect next servo to SERVOn pin next test ==")
    sleep(8)
    print("[INFO] - starting in 1 second")
    sleep(1)


print("[INFO] END - SERVO Test")
