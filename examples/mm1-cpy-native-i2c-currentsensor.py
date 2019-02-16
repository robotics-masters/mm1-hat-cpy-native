# CircuitPython Test for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython 3.1
#


import board
import digitalio
import time

import busio
import adafruit_ina219

i2c_bus = busio.I2C(board.SCL, board.SDA)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
    
# Create library object on our I2C port
ina219 = adafruit_ina219.INA219(i2c_bus, 0x41)


while True:
    led.value = True
    time.sleep(1)
    
    print("Bus Voltage:     {} V".format(ina219.bus_voltage))
    print("Shunt Voltage:   {} mV".format(ina219.shunt_voltage / 1000))
    print("Load Voltage:    {} V".format(ina219.bus_voltage + ina219.shunt_voltage))
    print("Current:         {} mA".format(ina219.current))
    print("")
    
    led.value = False
    time.sleep(4)
