from readchar import readkey
import serial
import numpy as np

arduino_connect = True

# some parameters
move_keys = {'w': [0,1,0],
            'a': [1,0,0],
            's': [0,-1,0],
            'd': [-1,0,0],
            'q': [0,0,-1],
            'e': [0,0,1]}

speed = np.array([500, 500, 500])


if arduino_connect is True:
    # initialisation the arduino connection
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.timeout = 1
    ser.port = '/dev/ttyACM0'
    ser.open()
    # change speed
    #ser.write('STV 1 {} {} {}'.format(speed[0], speed[1], speed[2]))
    #ser.readline()
    ser.flush()


# ToDO: use thread to control the motor rather than while True
while True:
    k = readkey()
    if k in move_keys.keys():
        if arduino_connect is True:
            ser.write('JOG 1 {} {} {} \r'.format(move_keys[k][0], move_keys[k][1], move_keys[k][2]).encode())
            print(ser.readline())
        else: 
            print('JOG 1 {} {} {} \r'.format(move_keys[k][0], move_keys[k][1], move_keys[k][2]).encode())
    
    elif k in ['x']:
        break

    # SPEED CONTROL DOESNT REALLY WORK FOR JOGGING. DISABLE FOR NOW
    '''
    elif k in (']','['): 
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
            print('JOG 1 {} {} {} \r'.format(speed[0], speed[1], speed[2]).encode())
    '''

