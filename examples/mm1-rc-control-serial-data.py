# CircuitPython Test for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython 4.0
#   Date: 15/05/2019
#
import time
import board
import busio

#from analogio import AnalogIn
from digitalio import DigitalInOut, Direction

from pulseio import PWMOut, PulseIn, PulseOut
from array import array
#from adafruit_motor import servo

## set up on-board LED
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

## set up serial UART
# note UART(TX, RX, baudrate)
uart = busio.UART(board.Pi_RX, board.Pi_TX, baudrate=9600)

## set up servos and radio control channels
steering_pwm = PWMOut(board.SERVO1, duty_cycle=2 ** 15, frequency=50)
throttle_pwm = PWMOut(board.SERVO2, duty_cycle=2 ** 15, frequency=50)

steering_servo = PulseOut(steering_pwm)
throttle_servo = PulseOut(throttle_pwm)

# TODO: move away from direct PusleOut.
#steering_servo = servo.Servo(pwm1)
#throttle_servo = servo.Servo(pwm2)

steering_channel = PulseIn(board.RCH1)
throttle_channel = PulseIn(board.RCH2)

## Set some other variables
DEBUG = False
throttle_servo.send(array('H', [1500]))

## Hardware Notification: starting
print("preparing to start..")
for i in range(0, 2):
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)

## GO TO: main()

## functions
def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def get_angle(time):
    # TODO: 1000ms==0°, 2000ms==270°. So: (ms-999)*1001/270
    return (time)/(18) + 7.5


def state_changed(ch, servo):
    ch.pause()
    data = array('H', [ch[0]])
    if DEBUG:
        print("data: ", data)
        print("data[0]: ", data[0])
    servo.send(data)
    del data
    ch.clear()
    ch.resume(2)

    
def main():
    throttle = False  # TODO: implement later
    # TODO: serial send data
    while True:

        # wait for data to be inputted by controller
        #   - break if the throttle channel has data
        #   - break if the steering channel has data
        #   - wait in loop if no data present
        while len(throttle_channel) == 0:
            if (len(steering_channel) != 0):
                state_changed(steering_channel, steering_servo)
            else:
                pass

        state_changed(throttle_channel, throttle_servo)

## Run
main()
