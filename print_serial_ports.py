import serial
import serial.tools.list_ports

available_ports = list(serial.tools.list_ports.comports())
for port in available_ports:
    print(port[0])
    print(port[1])
    if 'Micro' in port[1]:
        arduino_port = port[0]
        print('Fergus port: '+ arduino_port)


