# CircuitPython Test for Robotics Masters MM1
#
# Notes:
#   This is to be run using CircuitPython 4.0
#   Date: 15/06/2019
#
import board
import digitalio
import time
import busio

uart = busio.UART(board.GPS_TX, board.GPS_RX, baudrate=9600, timeout=1)
gps = busio.UART(board.UART_TX, board.UART_RX, baudrate=9600, timeout=1)

while True:
    data = uart.read(1)  # read up to 32 bytes
    # print(data)  # this is a bytearray type

    if data is not None:
        # convert bytearray to string
        data_string = ''.join([chr(b) for b in data])
        print(data_string, end="")
        gps.write(data)

    ext_data = gps.read(1)

    if ext_data is not None:
        ext_data_string = ''.join([chr(c) for c in ext_data])
        print(ext_data_string, end="")
