# Donkey Car Driver for Robotics Masters Robo HAT MM1
#
# Notes:
#   This is to be run using CircuitPython 5.0
#   Date: 15/05/2019
#   Updated: 02/12/2019
#
#

import time
import board
import busio

from digitalio import DigitalInOut, Direction
from pulseio import PWMOut, PulseIn, PulseOut

## Customisation these variables
SMOOTHING_INTERVAL_IN_S = 0.025
DEBUG = False
ACCEL_RATE = 10

## functions
def servo_duty_cycle(pulse_ms, frequency = 60):
	period_ms = 1.0 / frequency * 1000.0
	duty_cycle = int(pulse_ms / 1000 / (period_ms / 65535.0))
	return duty_cycle

def state_changed(control):
        prev = control.value
	control.channel.pause()
	for i in range(0, len(control.channel)):
		val = control.channel[i]
                # prevent ranges outside of control space
		if(val < 1000 or val > 2000):
			continue
		# set new value
		control.value = (control.value + val) / 2

	if DEBUG:
		print("%f\t%s (%i): %i (%i)" % (time.monotonic(), control.name, len(control.channel), control.value, servo_duty_cycle(control.value)))
	control.channel.clear()
	control.channel.resume()

def state_changed_throttle(control):
        prev = control.value
	control.channel.pause()
	for i in range(0, len(control.channel)):
		#val = control.channel[i]
                # prevent ranges outside of control space
		if(val < 1000 or val > 2000):
			continue
		# cap maximum acceleration to prevent stall
		#if (val - prev) > ACCEL_RATE:
                #        val = (control.value + ACCEL_RATE)
                # set new value
		control.value = (control.value + val) / 2

	if DEBUG:
		print("%f\t%s (%i): %i (%i)" % (time.monotonic(), control.name, len(control.channel), control.value, servo_duty_cycle(control.value)))
	control.channel.clear()
	control.channel.resume()

class Control:
     def __init__(self, name, servo, channel, value):
	self.name = name
	self.servo = servo
	self.channel = channel
	self.value = value
	self.servo.duty_cycle = servo_duty_cycle(value)

## set up on-board LED
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

## set up serial UART
# note UART(TX, RX, baudrate)
uart = busio.UART(board.TX1, board.RX1, baudrate = 115200, timeout = 0.001)

## set up servos and radio control channels
steering_pwm = PWMOut(board.SERVO2, duty_cycle = 2 ** 15, frequency = 60)
throttle_pwm = PWMOut(board.SERVO1, duty_cycle = 2 ** 15, frequency = 60)

steering_channel = PulseIn(board.RCC2, maxlen=64, idle_state=0)
throttle_channel = PulseIn(board.RCC1, maxlen=64, idle_state=0)

steering = Control("Steering", steering_pwm, steering_channel, 1500)
throttle = Control("Throttle", throttle_pwm, throttle_channel, 1500)

## Hardware Notification: starting
print("preparing to start...")
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
		if(last_update + SMOOTHING_INTERVAL_IN_S > time.monotonic()):
			continue
		last_update = time.monotonic()

		if(len(throttle.channel) != 0):
			#state_changed_throttle(throttle)
			state_changed(throttle)

		if(len(steering.channel) != 0):
			state_changed(steering)

		if(DEBUG):
			print("Get: %i, %i" % (int(steering.value), int(throttle.value)))
		uart.write(b"%i, %i\r\n" % (int(steering.value), int(throttle.value)))
		while True:
			byte = uart.read(1)
			if(byte == None):
				break
			last_input = time.monotonic()
			if(DEBUG):
				print("Read from UART: %s" % (byte))
			if(byte == b'\r'):
				data = bytearray('')
				datastr = ''
				break
			data[len(data):len(data)] = byte
			datastr = ''.join([chr(c) for c in data]).strip() # convert bytearray to string
		if(len(datastr) >= 10):
			steering_val = steering.value
			throttle_val = throttle.value
			try:
				steering_val = int(datastr[:4])
				throttle_val = int(datastr[-4:])
			except ValueError:
				None
				
			data=bytearray('')
			datastr = ''
			last_input = time.monotonic()
			if(DEBUG):
				print("Set: %i, %i" % (steering_val, throttle_val))

		if(last_input + 10 < time.monotonic()):
			steering.servo.duty_cycle = servo_duty_cycle(steering.value)
			throttle.servo.duty_cycle = servo_duty_cycle(throttle.value)
		else:
			steering.servo.duty_cycle = servo_duty_cycle(steering_val)
			throttle.servo.duty_cycle = servo_duty_cycle(throttle_val)


## Run
print("Run!")
main()
