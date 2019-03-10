# Robo HAT MM1 - CircuitPython Native

Examples and Firmware for the Robo HAT MM1 using CircuitPython on M0.

## Introduction

CircuitPython is an education friendly open source derivative of MicroPython. CircuitPython supports use on educational development boards designed and sold by Adafruit. [Adafruit CircuitPython](https://github.com/adafruit/circuitpython) features unified Python core APIs and a growing list of Adafruit libraries and drivers of that work with it.

## Build UF2 Bootloader

Please see the mm1-hat-cpy-native/uf2-bootloader folder for further instructions.

## Build CircuitPython

Please see the mm1-hat-cpy-native/firmware folder for further instructions.

## USB

This folder contains files that are needed to run the Robo HAT MM1.  The files are extra CircuitPython libraries that are not included in the standard build of CircuitPython.

**Libraries (lib)**

- adafruit_bus_device/
- adafruit_motor/
- adafruit_register/
- adafruit_ina219.mpy
- neopixel.mpy

There is also a copy of the full Adafruit Bundle for CircuitPython 4.0.0.  This will be removed in the future.
