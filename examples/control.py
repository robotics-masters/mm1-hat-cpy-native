# CircuitPython DonkeyCar Controller for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython >=6.2
#   Last Updated: 13/04/2021 (hmic)
#
# the controls used to interact with the RC receiver, servos and different motordrivers

## set up motor/servo outputs and pwm output channels
#button = Button()
#servo = Servo(board.SERVO1)
#motor = MotorDRV8871(board.SERVO4, board.SERVO3)
# or
#motor1 = MotorTB6621(board.SERVO1, board.SERVO2)
#motor2 = MotorTB6621(board.SERVO3, board.SERVO4)

## setup radio control input channels
#modeChangeButton = RCInput(board.RCC2, button.setPulse)
#steering = RCInput(board.RCC4, servo.setPulse)
#throttle = RCInput(board.RCC3, motor.setPulse)
## or
#mixer = Mixer(motor1, motor2)
#steering = RCInput(board.RCC4, mixer.setSteeringPulse)
#throttle = RCInput(board.RCC3, mixer.setThrottlePulse)

## in the main loop call the run functions periodically to process the RC input and update the attached outputs of the servo and motor(s)
#button.run()
#steering.run()
#throttle.run()

from digitalio import DigitalInOut, Direction
from pulseio import PWMOut, PulseIn

DEBUG = False

class RCInput():
	def __init__(self, rcPin, updateCallback = None):
		self._pulse = 1500 # center
		self.rc = PulseIn(rcPin, maxlen=16, idle_state=0)
		self.update_callback = updateCallback
	@property
	def pulse(self):
		return self._pulse
	@pulse.setter
	def pulse(self, pulse):
		self._pulse = pulse
		if(self.update_callback is not None):
			self.update_callback(pulse)

	def run(self, update = True):
		valid_pulse = False
		self.rc.pause()
		samples = len(self.rc)
		if(samples == 0):
			self.rc.resume()
			if(DEBUG):
				print("RCInput: No input from RC received (this might happen if you call run() too frequently and can be ignored in this case).")
			return False

		value = avg = self.pulse
		for i in range(0, samples):
			val = self.rc[i]
			# we (seem to) capture the length of the 0 pulse too (about 6000ms), filter for valid pulses
			if(val < 900 or val > 2100): # pulses get normalized afterwards anyways, but we want to filter invalid ones really
				continue
			valid_pulse = True
			value = val
			avg = (self.pulse + value) / 2 # average over the collected samples
		self.rc.clear()
		self.rc.resume()
		if DEBUG:
			print(f'RCInput: Got {samples} samples, last val={value}, current avg={self.pulse}{", valid" if valid_pulse else ""}{", update callback" if update else ""}')
		if(update):
			self.pulse = avg
		else:
			self._pulse = avg # don't call the update callback to change the attached servo/motor
		return valid_pulse

class BaseControl:
	def __init__(self, updateCallback = None):
		self.update_callback = updateCallback
		self._pulse = 1500 # center
		self._value = 0 # center (off)

	@property
	def pulse(self):
		return self._pulse
	@pulse.setter
	def pulse(self, pulse):
		self._pulse = self.normalize_pulse(pulse) # range 1000 to 2000

	# we need a function distinct from the actual setter to make it a callable, we can as well add an extra parameter now
	def setPulse(self, pulse, update_value = True):
		self.pulse = pulse
		value = self.pulseToValue(pulse)
		if(update_value):
			self.value = value
		return value

	@property
	def value(self):
		return self._value
	@value.setter
	def value(self, value):
		if(value >= -100 and value <= 100):
			self._value = value
			if(self.update_callback is not None):
				self.update_callback(value)
				if(DEBUG):
					print("Control: Called update callback.")
		else:
			if(DEBUG):
				print(f'Control: Invalid value: {value}, ignored.')

	def normalize_pulse(self, pulse_ms, min = 1000, max = 2000):
		if(pulse_ms < min):
			return min  # if the pulse length is too short, cap it at minimum
		if(pulse_ms > max):
			return max  # if the pulse length is too long, cap it at maximum
		return pulse_ms # return the valid pulse length
	def pulseToValue(self, pulse_ms):
		pulse = self.normalize_pulse(pulse_ms)
		value = (pulse - 1500) / 5.0 # range -100 to 100
		return value

## a mixer to drive 2 motors from throttle and steering values
class Mixer:
	def __init__(self, leftControl, rightControl):
		self.throttle_value = 0
		self.steering_value = 0
		self.leftMotor = leftControl
		self.rightMotor = rightControl

	def setThrottlePulse(self, pulse):
		self.throttle_value = self.leftMotor.pulseToValue(pulse)
		if DEBUG:
		    print(f'Mixer: Set throttle {self.throttle_value}')
		self.updateMotors()

	def setSteeringPulse(self, pulse):
		self.steering_value = self.leftMotor.pulseToValue(pulse)
		if DEBUG:
			print(f'Mixer: Set steering: {self.steering_value}')
		self.updateMotors()

	def updateMotors(self):
		factor = 1 / 1.4142 # or use just 1...
		if(self.steering_value < 0):
			factor = -factor # or factor *= -1
		if(self.throttle_value < 0):
			factor = -factor # or factor *= -1

		left_value = self.throttle_value + abs(self.steering_value) * factor
		if(left_value > 100):
			left_value = 100
		if(left_value < -100):
			left_value = -100
		right_value = self.throttle_value + abs(self.steering_value) * -factor
		if(right_value > 100):
			right_value = 100
		if(right_value < -100):
			right_value = -100

		if DEBUG:
			print(f'Mixer: Update motors: {left_value}, {right_value}')
		self.leftMotor.value = left_value
		self.rightMotor.value = right_value

## a button/switch on the remote (toggle)
class Button(BaseControl):
	def __init__(self, switchMode = True, updateCallback = None, buttonSwing = 150):
		self.update_fkt = updateCallback
		super().__init__(self.update)
		self.last_value = buttonSwing / 2
		self.pressed = False
		self.button_swing = buttonSwing
		self.switch_mode = switchMode
	def update(self, value):
		if(not self.switch_mode):
			self.pressed = value > self.button_swing / 2
		elif(value - self.button_swing > self.last_value or value + self.button_swing < self.last_value):
			self.last_value = value
			self.pressed = True
		if(self.update_fkt is not None):
			self.update_fkt(value)
	def get_pressed(self):
		pressed = self.pressed
		if(self.switch_mode):
			self.pressed = False
		return pressed

## rc servo driver
class Servo(BaseControl):
	def __init__(self, pwmPin, updateCallback = None):
		self.update_fkt = updateCallback
		super().__init__(self.update)
		self.pwm = PWMOut(pwmPin, duty_cycle = self.duty_cycle, frequency = 60)
	def update(self, value):
		#if(self.pwm is None):
		#	pass
		if(self.update_fkt is not None):
			self.update_fkt(value)
		self.pwm.duty_cycle = self.duty_cycle
	@property
	def duty_cycle(self):
		period_ms = 1000.0 / self.pwm.frequency
		duty_cycle = (self.value + 100) # range 100 to 200
		return int(duty_cycle / (period_ms / 655.35))

## motor driver with pwm and direction pins
class MotorDRV8871(BaseControl):
	def __init__(self, pwmPin, dirPin, updateCallback = None):
		self.update_fkt = updateCallback
		super().__init__(self.update)
		self.dir = DigitalInOut(dirPin)
		self.dir.direction = Direction.OUTPUT
		self.pwm = PWMOut(pwmPin, duty_cycle = self.duty_cycle, frequency = 1000)
	def update(self, value):
		#if(self.pwm is None):
		#	pass
		if(self.update_fkt is not None):
			self.update_fkt(value)
		self.pwm.duty_cycle = self.duty_cycle
	@property
	def duty_cycle(self):
		if(self.value < 0): # backwards
			duty_cycle = -self.value # range 0 to 100
			self.dir.value = False
		# at the center spot duty_cycle will switch from 0 to 65535, need to change the self.dir.value
		if(self.value >= 0): # forwards
			duty_cycle = self.value # range 0 to 100
			self.dir.value = True
		return int(duty_cycle * 655.35) # range 0 to 65535

## motor driver with two pwm pins
class MotorTB6621(BaseControl):
	def __init__(self, pin1, pin2, updateCallback = None):
		self.update_fkt = updateCallback
		super().__init__(self.update)
		left_duty, right_duty = self.duty_cycle
		self.pin1 = PWMOut(pin1, duty_cycle = left_duty, frequency = 1000)
		self.pin2 = PWMOut(pin2, duty_cycle = right_duty, frequency = 1000)
	def update(self, value):
		#if(self.pin1 is None or self.pin2 is None):
		#	pass
		if(self.update_fkt is not None):
			self.update_fkt(self.value)
		self.pin1.duty_cycle, self.pin2.duty_cycle = self.duty_cycle
	@property
	def duty_cycle(self):
		if(self.value < 0): # backwards
			duty_cycle1 = -self.value # range 0 to 100
			duty_cycle2 = 0
		if(self.value >= 0): # forwards
			duty_cycle1 = 0
			duty_cycle2 = self.value  # range 0 to 100
		return int(duty_cycle1 * 655.35), int(duty_cycle2 * 655.35) # range 0 to 65535
