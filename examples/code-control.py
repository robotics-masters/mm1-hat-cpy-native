# CircuitPython DonkeyCar Controller for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython >=6.2
#   Last Updated: 13/04/2021 (hmic)
#

import time
import board
import busio
import gamepad
import microcontroller

from digitalio import DigitalInOut, Direction, Pull
from control import RCInput, Mixer, Button, Servo, MotorDRV8871, MotorTB6621

## set up serial UART, note UART(TX, RX, ...)
## at 115200 bits per second a timeout of 1ms would allow for more than 11 bits to be transferred ("at least a byte")
uart = busio.UART(board.PI_TX, board.PI_RX, baudrate = 115200, timeout = 0.001)

## set up on-board LED
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

## set up "power" button
dbutton = DigitalInOut(board.BUTTON)
dbutton.switch_to_input(pull = Pull.DOWN)
#button = gamepad.GamePad(dbutton)

## set up motor/servo outputs and pwm output channels
#motor = MotorDRV8871(board.SERVO4, board.SERVO3)
#motor = Servo(board.SERVO2)
#servo = Servo(board.SERVO1)
button = Button()

motor1 = MotorTB6621(board.SERVO1, board.SERVO2)
motor2 = MotorTB6621(board.SERVO3, board.SERVO4)

## setup radio control input channels
#throttle = RCInput(board.RCC3, motor.setPulse)
#steering = RCInput(board.RCC4, servo.setPulse)
modeChangeButton = RCInput(board.RCC2, button.setPulse)

mixer = Mixer(motor1, motor2)
throttle = RCInput(board.RCC3, mixer.setThrottlePulse)
steering = RCInput(board.RCC4, mixer.setSteeringPulse)

## Set some other variables
DEBUG = False
SPEED_FACTOR = 1
MAX_LOOP_UPDATE_SPEED_HZ = 50
if(DEBUG):
	MAX_LOOP_UPDATE_SPEED_HZ = 5

last_press = time.monotonic()
remotecontrol_active = True
def check_remotecontrol_mode():
	global remotecontrol_active, last_press
	# use the RC to change remote control mode or (just) use the "power" button on the car instead
	# by commenting out this line and use the GamePad button above instead
	modeChangeButton.run()
	if(button.get_pressed() and last_press + 0.33 < time.monotonic()):
		remotecontrol_active = not remotecontrol_active
		last_press = time.monotonic()
	return remotecontrol_active

serial_data_buffer = bytearray('')
def get_serial_command(uart, steering_pulse, throttle_pulse):
	global serial_data_buffer

	steering = steering_pulse
	throttle = throttle_pulse
	valid = False
	while True:
		byte = uart.read(1)
		if(byte == None):
			break
		if(byte == b'\r'):
			serial_data_buffer = bytearray('')
			continue
		l = len(serial_data_buffer)
		serial_data_buffer[l:l] = byte
		# excpected format: "1234, 1234\r"
		if(l + 1 == 10): # this only works if we got the start right, check above discarding of the data array on receiving \r
			try:
				str = ''.join([chr(c) for c in serial_data_buffer]).strip() # convert bytearray to string
				steering = int(str[:4])
				throttle = int(str[-4:])

				valid = True
				if(DEBUG):
					print(f'Serial data, read: steering={steering}, throttle={throttle}')
			except ValueError:
				# fallback, use current data if the serial data received turns out to be invalid
				steering = steering_pulse
				throttle = throttle_pulse
				if(DEBUG):
					print(f'Invalid serial data: {"".join([chr(b) for b in data]).strip()}')
			data = bytearray('')
	return steering, throttle, valid

def main():
	# initialize variables
	last_update = time.monotonic()
	led.value = remotecontrol_active

	while True:
		if(last_update + (1.0 / MAX_LOOP_UPDATE_SPEED_HZ) > time.monotonic()):
			if(DEBUG):
				time.sleep(0.1 / MAX_LOOP_UPDATE_SPEED_HZ)
				print("~", end="")
			continue
		if(DEBUG):
			print("")
		last_update = time.monotonic()

		led.value = check_remotecontrol_mode()

		steering_valid = steering.run(remotecontrol_active)
		throttle_valid = throttle.run(remotecontrol_active) # the receiver outputs center throttle data with the sender turned off (as a safety measure?!)
		if(steering_valid and throttle_valid):
			if(DEBUG):
				print(f'Remotecontrol data (active: {remotecontrol_active}): steering={steering.pulse}, throttle={throttle.pulse}')
			if(remotecontrol_active or (not remotecontrol_active and ((steering.pulse < 1480 or steering.pulse > 1520) or (throttle.pulse < 1480 or throttle.pulse > 1520)) ) ):
				# always send current remotecontrol data to serial (if it's sending data?!)
				uart.write(b"%i, %i\r\n" % (int(steering.pulse), int(throttle.pulse)))

		steering_val, throttle_val, serial_valid = get_serial_command(uart, steering.pulse, throttle.pulse)
		if(serial_valid and not remotecontrol_active):
			steering.pulse = steering_val
			throttle.pulse = throttle_val * SPEED_FACTOR
			if(DEBUG):
				print(f'Set serial data: steering={steering.pulse}, throttle={throttle.pulse}')

## Hardware Notification: starting
print("Get ready to start...")
for i in range(0, 5):
	led.value = not led.value
	time.sleep(0.33)
## Run
print(f'ID: {"".join("%02x" % b for b in microcontroller.cpu.uid)}')
print("Run!")
main()
