# CircuitPython Firmware
Use with https://github.com/adafruit/circuitpython

### ports/atmel-samd/board/roboticsmasters_mm1/

## Build Steps

```
git clone https://github.com/adafruit/circuitpython/
cd circuitpython/ports/atmel-samd
git submodule update --init --recursive
make -C mpy-cross

make BOARD=roboticsmasters_mm1
```

## Output

```
ports/atmel-samd/builds
```