# CircuitPython Demo - USB/Serial Debugger
 
import board
import busio
import digitalio
 
 
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
 
uart = busio.UART(board.TX, board.RX, baudrate=9600)

print("Running Debugger")

while True:
    data = uart.read(32)  # read up to 32 bytes
    dataSend = local.read(32)
    # print(data)  # this is a bytearray type

    if data is not None:
        led.value = True
 
        # convert bytearray to string
        data_string = ''.join([chr(b) for b in data])
        print(data_string, end="")
 
        led.value = False
        
    
