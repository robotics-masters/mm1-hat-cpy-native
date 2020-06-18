import board
import digitalio
import time
import busio

# setup I2C
i2c = busio.I2C(board.SCL, board.SDA)

while True:
    while not i2c.try_lock():
        pass

    [print(hex(x)) for x in i2c.scan()]

    i2c.unlock()

    time.sleep(3)

