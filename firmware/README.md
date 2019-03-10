# CircuitPython Firmware
Use with https://github.com/adafruit/circuitpython


## Set Up Build Environment

Until our library is allowed to be included into the adafruit/seesaw repository, you must clone this repository and the seesaw repository.

```
git clone https://github.com/robotics-masters/mm1-hat-cpy-native
git clone https://github.com/adafruit/circuitpython/
cd circuitpython/
git submodule update --init --recursive
make -C mpy-cross
cd circuitpython/ports/atmel-samd
cp -r ../../../mm1-hat-cpy-native/firmware/mm1_hat_nonflash boards/mm1_hat_nonflash
```

## Build Steps

The default board is `debug`. You can build a different one using:

```
make -j8 BOARD=mm1_hat_nonflash
```

**Note:** We support a few different varients of the Robo HAT MM1.  Check you are using the correct one.

Further instruction: https://learn.adafruit.com/building-circuitpython/build-circuitpython

## Output

```
ports/atmel-samd/builds
```
