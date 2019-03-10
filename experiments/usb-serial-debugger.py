# CircuitPython Demo - USB/Serial Debugger
 
import board
import busio
import digitalio
 
uart = busio.UART(board.TX, board.RX, baudrate=115200)

print("Running Debugger")

while True:
    data = uart.read(32)  # read up to 64 bytes
    #print(data)  # this is a bytearray type

    if data is not None:
        # convert bytearray to string
        data_string = ''.join([chr(b) for b in data])
        print(data_string, end="")

        
    
