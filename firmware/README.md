# CircuitPython Firmware
Use with https://github.com/adafruit/circuitpython

### ports/atmel-samd/board/roboticsmasters_mm1/

## Build Steps

As per: https://learn.adafruit.com/building-circuitpython/build-circuitpython

```
git clone https://github.com/adafruit/circuitpython/

git submodule update --init --recursive

make -C mpy-cross

cd circuitpython/ports/atmel-samd

make BOARD=roboticsmasters_mm1
```

## Output

```
ports/atmel-samd/builds
```