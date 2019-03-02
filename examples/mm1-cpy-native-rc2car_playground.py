# CircuitPython Test for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython 3.1
#
import time
import board

from analogio import AnalogIn
from digitalio import DigitalInOut, Direction

from pulseio import PWMOut, PulseIn, PulseOut
from adafruit_motor import servo
from array import array

# set up on-board LED
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT


# set up servos and radio control channels

pwm1 = PWMOut(board.SERVO1, duty_cycle=2 ** 15, frequency=50)
pwm2 = PWMOut(board.SERVO2, duty_cycle=2 ** 15, frequency=50)
#steering_servo = servo.Servo(pwm1)
#throttle_servo = servo.Servo(pwm2)
steering_servo = PulseOut(pwm1)
throttle_servo = PulseOut(pwm2)

steering_channel = PulseIn(board.RCH1)
throttle_channel = PulseIn(board.RCH2)


# functions
def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def get_angle(time):
    return (time)/(18) + 7.5

def get_range(pulse):
    if 1540 < pulse < 1580:
        return 1566
    elif pulse > 1580:
        return 1650
    elif pulse < 1540:
        return 1450

# TESTS
#  This runs in the following order:
#   1. Get value from both RCH
#   2. Send to respective servos
#   3. Send to Raspberry Pi (if connected)
#
# Then the test repeats.


## go-loop

#ch1 = array('H', [1500])
ch2 = array('H', [1500])

while True:
    # get radio channel values
    #steering_servo.angle = get_angle(steering_channel)
    #throttle_servo.angle = get_angle(throttle_channel)
    
    ### working between here and next comment
    while len(throttle_channel) == 0:
        pass
    
    throttle_channel.pause()
    
    print(throttle_channel[0])
    
    throttle_servo.send(array('H', [(throttle_channel[0])]))
    #throttle_servo.angle = get_angle(steering_channel[0])
    
    
    #throttle_channel.clear()
    
    throttle_channel.resume()
    
    time.sleep(0.01)
    ### working between here and last comment
    
    # while len(steering_channel) == 0 or len(throttle_channel) == 0:
#         if len(steering_channel) > 0: break
#         elif len(throttle_channel) > 0: break
#         else: pass
    
    ### steering
    #if len(steering_channel) > 0:
    #    steering_channel.pause()
    #    ##ch1[0] = steering_channel[0]
    #    print("Steering ",  steering_channel[0])
    #    ##steering_servo.angle = get_angle(steering_channel[0])
    #    steering_channel.clear()
    #    steering_channel.resume(20000)
    
    ### throttle
    #if len(throttle_channel) > 0:
    #    throttle_channel.pause()
    #    ##ch2[0] = throttle_channel[0]
    #    print("Throttle ",  throttle_channel[0])
    #    ##throttle_servo.angle = get_angle(throttle_channel[0])
    #    throttle_channel.clear()
    #    throttle_channel.resume(20000)

    #time.sleep(0.01)
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
