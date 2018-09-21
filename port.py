import serial
ser = serial.Serial()
ser.baudrate = 115200
ser.timeout = 5
ser.port = '/dev/ttyACM0'
ser.open()
# /r is very important here
ser.write('MOV 1 500 500 500 \r\n'.encode())

while True:
    ser.write('JOG 1 1 0 0 \r\n'.encode())
    print(ser.readline())
