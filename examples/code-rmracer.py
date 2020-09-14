# CircuitPython DonkeyCar Controller for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython 5.0
#   Date: 19/06/2020
#
import time
import board
import busio

from digitalio import DigitalInOut, Direction
from pulseio import PWMOut, PulseIn, PulseOut


## functions
def servo_duty_cycle(pulse_ms, frequency = 60):
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
	def __init__(self, name, servo, channel, value, update_function):
		self.name = name
		self.servo = servo
		# channel.pause()
		# channel.clear()
		# channel.resume(100)
		self.channel = channel
		self.value = value
		self.servo.duty_cycle = update_function(value)
		self.update_function = update_function
	def duty_cycle(self, value):
		self.servo.duty_cycle = self.update_function(value)
		return self.servo.duty_cycle
	def state_changed(self):
		# self.channel.pause()
		for i in range(0, len(self.channel)):
			val = self.channel[i]
			if(val < 1000 or val > 2000):
				continue
			# self.value = (self.value + val) / 2
			self.value = val
		if DEBUG:
			print("%f\t%s (%i): %i (%i) %i" % (time.monotonic(), self.name, len(self.channel), self.value, self.duty_cycle(self.value), motor_direction.value))
		self.channel.clear()
		# self.channel.resume()


## set up on-board LED
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

## set up serial UART
# note UART(TX, RX, baudrate)
uart = busio.UART(board.PI_TX, board.PI_RX, baudrate = 115200, timeout = 0.001)

## set up servo/motor outputs
motor_direction = DigitalInOut(board.SERVO3)
motor_direction.direction = Direction.OUTPUT
motor_direction.value = False
throttle_pwm = PWMOut(board.SERVO4, duty_cycle = motor_duty_cycle(1500), frequency = 500)
steering_pwm = PWMOut(board.SERVO2, duty_cycle = servo_duty_cycle(1500), frequency = 60)

# setup radio control channels
throttle_channel = PulseIn(board.RCC3, maxlen=16, idle_state=0)
steering_channel = PulseIn(board.RCC4, maxlen=16, idle_state=0)

steering = Control("Steering", steering_pwm, steering_channel, 1500, servo_duty_cycle)
throttle = Control("Throttle", throttle_pwm, throttle_channel, 1500, motor_duty_cycle)

## Set some other variables
SPEED_FACTOR = 1
SMOOTHING_INTERVAL_IN_S = 0.05
DEBUG = True
last_update = time.monotonic()

## Hardware Notification: starting
print("Preparing to start...")
for i in range(0, 2):
	led.value = True
	time.sleep(0.5)
	led.value = False
	time.sleep(0.5)

## GO TO: main()
def main():
	global last_update

	data = bytearray('')
	datastr = ''
	last_input = 0
	steering_val = steering.value
	throttle_val = throttle.value

	while True:
		# time.sleep(0.5)
		if(last_update + SMOOTHING_INTERVAL_IN_S > time.monotonic()):
			continue

		last_update = time.monotonic()

		changed = False
		if(len(throttle.channel) != 0):
			throttle.state_changed()
			changed = True

		if(len(steering.channel) != 0):
			steering.state_changed()
			changed = True

		if(changed):
			if(DEBUG):
				print("Get: %i, %i" % (int(steering.value), int(throttle.value)))
		uart.write(b"%i, %i\r\n" % (int(steering.value), int(throttle.value)))

		while True:
			byte = uart.read(1)
			if(byte == None):
				break
			# last_input = time.monotonic()
			if(DEBUG):
				print("Read from UART: %s" % (byte))
			if(byte == b'\r'):
				data = bytearray('')
				datastr = ''
				break
			data[len(data):len(data)] = byte
			if(len(data) >= 10):
				datastr = ''.join([chr(c) for c in data]).strip() # convert bytearray to string
				steering_val = steering.value
				throttle_val = throttle.value
				try:
					steering_val = int(datastr[:4])
					throttle_val = int(datastr[-4:]) * SPEED_FACTOR
					last_input = time.monotonic()
				except ValueError:
					None
				data=bytearray('')
				datastr = ''


				if(DEBUG):
					print("Set: %i, %i" % (steering_val, throttle_val))

		if(last_input + 10 < time.monotonic()):
			steering.duty_cycle(steering.value)
			throttle.duty_cycle(throttle.value)
			print(last_input)
		else:
			steering.duty_cycle(steering_val)
			throttle.duty_cycle(throttle_val)
			print(last_input)
			print(2)

## Run
print("Run!")
main()

