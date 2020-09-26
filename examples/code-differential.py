# Donkey Car Driver for Robotics Masters Robo HAT MM1
#
# Notes:
#   This is to be run using CircuitPython 5.x
#   Date: 15/05/2019
#   Updated: 14/09/2020 (wallarug)
#

import time
import board
import busio

from digitalio import DigitalInOut, Direction
from pulseio import PWMOut, PulseIn, PulseOut

import adafruit_logging as logging
logger = logging.getLogger('code')
logger.setLevel(logging.INFO)

# Customisation these variables
DEBUG = False
USB_SERIAL = False
SMOOTHING_INTERVAL_IN_S = 0.025
ACCEL_RATE = 10

## cannot have DEBUG and USB_SERIAL
if USB_SERIAL:
    DEBUG = False

## functions
def servo_duty_cycle(pulse_ms, frequency = 60):
    """
    Formula for working out the servo duty_cycle at 16 bit input
    """
    if(pulse_ms > 2000 or pulse_ms < 1000):
	pulse_ms = 1500  # if the pulse length is invalid, set middle position
    period_ms = 1.0 / frequency * 1000.0
    duty_cycle = int(pulse_ms / 1000 / (period_ms / 65535.0))
    return duty_cycle

def motor_duty_cycle(pulse, frequency = 500):
	duty_cycle = 0
	if(pulse > 2000 or pulse < 1000):
		return duty_cycle # if the pulse length is invalid, 0% duty cycle to turn the motor off
	if(pulse < 1500):
		motor_direction.value = False
		duty_cycle = (1500 - pulse) / 500
	if(pulse > 1500):
		motor_direction.value = True
		duty_cycle = (2000 - pulse) / 500
	# here duty_cycle is between 0 and 100
	return int(duty_cycle * 65535.0)

class Control:
    """
    Class for a RC Control Channel
    """

    def __init__(self, name, servo, channel, value, update_function):
        self.name = name
        self.servo = servo
        self.channel = channel
        self.value = value
        self.servo.duty_cycle = update_function(value)
        self.update_function = update_function

    def duty_cycle(self, value):
	self.servo.duty_cycle = self.update_function(value)
	return self.servo.duty_cycle
	    
    def state_changed(self):
        """
        Reads the RC channel and smooths value
        """
        self.channel.pause()
        for i in range(0, len(self.channel)):
            val = self.channel[i]
            # prevent ranges outside of control space
            if(val < 1000 or val > 2000):
                continue
            # set new value
            self.value = val

        if DEBUG:
            logger.debug("%f\t%s (%i): %i (%i)" % (time.monotonic(), self.name, len(
                self.channel), self.value, self.servo_duty_cycle(self.value)))
        self.channel.clear()
        #control.channel.resume()


# set up on-board LED
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

# set up serial UART to Raspberry Pi
# note UART(TX, RX, baudrate)
uart = busio.UART(board.TX1, board.RX1, baudrate=115200, timeout=0.001)

## set up servo/motor outputs
## For differential you will be using two motors, no servos
## Pins are:
motor_direction_left = DigitalInOut(board.SERVO3)
motor_direction_left.direction = Direction.OUTPUT
motor_direction_left.value = False

motor_direction_right = DigitalInOut(board.SERVO4)
motor_direction_right.direction = Direction.OUTPUT
motor_direction_right.value = False

left_motor = PWMOut(board.SERVO2, duty_cycle = motor_duty_cycle(1500), frequency = 500)
right_motor = PWMOut(board.SERVO1, duty_cycle = motor_duty_cycle(1500), frequency = 500)

# set up RC channels.  NOTE: input channels are RCC3 & RCC4 (not RCC1 & RCC2)
throttle_channel = PulseIn(board.RCC3, maxlen=64, idle_state=0)
steering_channel = PulseIn(board.RCC4, maxlen=64, idle_state=0)


# setup Control objects.  1500 pulse is off and center steering
# ASSUMPTION - left motor is on steering, right motor on throttle (for code purposes)
steering = Control("Steering", left_motor, steering_channel, 1500, motor_duty_cycle)
throttle = Control("Throttle", right_motor, throttle_channel, 1500, motor_duty_cycle)

## Set some other variables
SPEED_FACTOR = 1
SMOOTHING_INTERVAL_IN_S = 0.05
DEBUG = True
last_update = time.monotonic()


# Hardware Notification: starting
logger.info("preparing to start...")
for i in range(0, 2):
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)

last_update = time.monotonic()

# GOTO: main()
def main():
    global last_update

    data = bytearray('')
    datastr = ''
    last_input = 0
    steering_val = steering.value
    throttle_val = throttle.value

    while True:
        # only update every smoothing interval (to avoid jumping)
        if(last_update + SMOOTHING_INTERVAL_IN_S > time.monotonic()):
            continue
        last_update = time.monotonic()

        # check for new RC values (channel will contain data)
        changed = False
        if(len(throttle.channel) != 0):
            throttle.state_changed()
            changed = True

        if(len(steering.channel) != 0):
            steering.state_changed()
            changed = True

        if DEBUG:
            logger.info("Get: steering=%i, throttle=%i" % (int(steering.value), int(throttle.value)))
        
        if(USB_SERIAL):
            # simulator USB
            print("%i, %i" % (int(steering.value), int(throttle.value)))
        else:
            # write the RC values to the RPi Serial
            uart.write(b"%i, %i\r\n" % (int(steering.value), int(throttle.value)))

        while True:
            # wait for data on the serial port and read 1 byte
            byte = uart.read(1)

            # if no data, break and continue with RC control
            if(byte == None):
                break
            #last_input = time.monotonic()

            if (DEBUG):
                logger.debug("Read from UART: %s" % (byte))

            # if data is recieved, check if it is the end of a stream
            if(byte == b'\r'):
                data = bytearray('')
                break

            data[len(data):len(data)] = byte

            # convert bytearray to string
            datastr = ''.join([chr(c) for c in data]).strip()

        # if we make it here, there is serial data from the previous step
        if(len(datastr) >= 10):
            steering_val = steering.value
            throttle_val = throttle.value
            try:
                steering_val = int(datastr[:4])
                throttle_val = int(datastr[-4:]) * SPEED_FACTOR
                last_input = time.monotonic()
            except ValueError:
                None

            data = bytearray('')
            datastr = ''
            logger.info("Set: steering=%i, throttle=%i" % (steering_val, throttle_val))

        if(last_input + 10 < time.monotonic()):
            # set the servo for RC control
            # TODO - add in diff code here
            left_val = throttle.value - (1500 - steering.value)
            right_val = throttle.value + (1500 - steering.value)
            steering.duty_cycle(left_val)
            throttle.duty_cycle(right_val)
        else:
            # set the servo for serial data (recieved)
            left_val = throttle.value - (1500 - steering.value)
            right_val = throttle.value + (1500 - steering.value)
            steering.duty_cycle(left_val)
            throttle.duty_cycle(right_val)


# Run
logger.info("Run!")
main()
