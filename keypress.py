from readchar import readkey
import serial
import numpy as np

# we can also use the code without arduino connection for debugging 
arduino_connect = False

# some parameters
move_keys = {'w': [0,1,0],
            'a': [1,0,0],
            's': [0,-1,0],
            'd': [-1,0,0],
            'q': [0,0,-1],
            'e': [0,0,1]}

speed = np.array([200, 200, 200])


if arduino_connect is True:
    # initialisation the arduino connection
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.timeout = 5
    ser.port = '/dev/ttyACM0'
    ser.open()
    ser.flush()
    # change speed
    ser.write('STV 1 {} {} {}'.format(speed[0], speed[1], speed[2]))
    ser.readline()


while True:
    k = readkey()
    if k in move_keys.keys():
        if arduino_connect is True:
            ser.write('JOG 1 {} {} {} \r'.format(move_keys[k][0], move_keys[k][1], move_keys[k][2]).encode())
        else: 
            print('JOG 1 {} {} {} \r'.format(move_keys[k][0], move_keys[k][1], move_keys[k][2]).encode())

    elif k in (']','['): 
        if k == ']':
            speed = speed*2
        elif k == '[':
            speed = speed/2
        print('speed: {}'.format(speed))
        if arduino_connect is True:
            ser.write('STV 1 {} {} {}'.format(speed[0], speed[1], speed[2]))
        else: 
            print('JOG 1 {} {} {} \r'.format(speed[0], speed[1], speed[2]).encode())
        

    elif k in ['x']:
        break

    # SPEED CONTROL DOESNT REALLY WORK FOR JOGGING. DISABLE FOR NOW

    """ elif k in (']','['): 
        if k == ']':
            speed = speed*1.25
        elif k == '[':
            speed = speed*0.8
        print('speed: {}'.format(speed))
        if arduino_connect is True:
            ser.write('STV 1 {} {} {}'.format(speed[0], speed[1], speed[2]))
            print(ser.readline())
            ser.flush()
        else: 
            print('JOG 1 {} {} {} \r'.format(speed[0], speed[1], speed[2]).encode()) """