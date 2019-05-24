# CircuitPython Test for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython 4.0
#   Date: 24/05/2019
#
import time
import board
import busio
import neopixel

from digitalio import DigitalInOut, Direction
from pulseio import PWMOut, PulseIn, PulseOut

## set up on-board LED
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

## set up NeoPixel LEDs
pixel_pin = board.NEOPIXEL
num_pixels = 6
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
ORANGE = (255, 127, 80)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pixels.fill(BLACK)
pixels.show()

## Pixel Map
# 0 Left Indicator
# 1 Left Break
# 2 Left Reverse
# 3 Right Reverse
# 4 Right Break
# 5 Right Indicator


## set up serial UART
# note UART(TX, RX, baudrate)
uart = busio.UART(board.PI_RX, board.PI_TX, baudrate = 115200, timeout = 0.001)

## set up servos and radio control channels
steering_pwm = PWMOut(board.SERVO1, duty_cycle = 2 ** 15, frequency = 50)
throttle_pwm = PWMOut(board.SERVO2, duty_cycle = 2 ** 15, frequency = 50)

steering_channel = PulseIn(board.RCH1, maxlen=64, idle_state=0)
throttle_channel = PulseIn(board.RCH2, maxlen=64, idle_state=0)

## Set some other variables
SMOOTHING_INTERVAL_IN_S = 0.025
DEBUG = True
last_update = time.monotonic()

## Hardware Notification: starting
print("preparing to start...")
for i in range(0, 2):
	led.value = True
	time.sleep(0.5)
	led.value = False
	time.sleep(0.5)

## GO TO: main()

## functions
def servo_duty_cycle(pulse_ms, frequency = 50):
	period_ms = 1.0 / frequency * 1000.0
	duty_cycle = int(pulse_ms / 1000 / (period_ms / 65535.0))
	return duty_cycle

def pix_logic_indicator(val):
        ## Left and Right (Indicators), Give: Steering
        if val < 1350:
                pixels[0] = BLACK
                pixels[5] = YELLOW
        elif val > 1650:
                pixels[0] = YELLOW
                pixels[5] = BLACK
        else:
                pixels[0] = BLACK
                pixels[5] = BLACK
        pixels.show()
        

def pix_logic_break(cur, prev):
        ## Backwards and Forwards (Breaking), Give: Throttle(s)
        reverse = pixels[2][0] # 255 is reverse

        if reverse is 255:
                if prev > cur:
                        pixels[1] = RED
                        pixels[4] = RED
                else:
                        pixels[1] = BLACK
                        pixels[4] = BLACK
        else:
                if prev < cur:
                        pixels[1] = RED
                        pixels[4] = RED
                else:
                        pixels[1] = BLACK
                        pixels[4] = BLACK
        pixels.show()
        

def pix_logic_reverse(val):
        ## Backwards (Reversing), Give: Throttle
        if val < 1400:
                pixels[2] = WHITE
                pixels[3] = WHITE
        else:
                pixels[2] = BLACK
                pixels[3] = BLACK
        pixels.show()
        

def state_changed(control):
	control.channel.pause()
	for i in range(0, len(control.channel)):
		val = control.channel[i]
		if(val < 1000 or val > 2000):
			continue
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

steering = Control("Steering", steering_pwm, steering_channel, 1500)
throttle = Control("Throttle", throttle_pwm, throttle_channel, 1000)

def main():
	global last_update
	
	data = bytearray('')
	datastr = ''
	last_input = 0
	steering_val = steering.value
	throttle_val = throttle.value

	while True:
                ## RC Controller Input
		if(last_update + SMOOTHING_INTERVAL_IN_S > time.monotonic()):
			continue
		last_update = time.monotonic()

		if(len(throttle.channel) != 0):
			state_changed(throttle)

		if(len(steering.channel) != 0):
			state_changed(steering)

		if(DEBUG):
			print("Get: %i, %i" % (int(steering.value), int(throttle.value)))
		uart.write(b"%i, %i\r\n" % (int(steering.value), int(throttle.value)))

		## Serial Input
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

                ## Servo Output
		if(last_input + 10 < time.monotonic()):
			steering.servo.duty_cycle = servo_duty_cycle(steering.value)
			throttle.servo.duty_cycle = servo_duty_cycle(throttle.value)
			pix_logic_reverse(throttle.value)
			pix_logic_indicator(steering.value)
		else:
			steering.servo.duty_cycle = servo_duty_cycle(steering_val)
			throttle.servo.duty_cycle = servo_duty_cycle(throttle_val)
			pix_logic_reverse(throttle_val)
			pix_logic_indicator(steering_val)


## Run
print("Run!")
main()
