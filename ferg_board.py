import numpy as np
import serial
import time
from readchar import readkey


def ferg_board_key_input(arduino_connect = False, pressed_key = None):
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
        ferg_board_ser = serial.Serial()
        ferg_board_ser.baudrate = 115200
        ferg_board_ser.timeout = 5
        ferg_board_ser.port = '/dev/ttyACM0'
        ferg_board_ser.open()
        ferg_board_ser.flush()
        # change speed
        ferg_board_ser.write('STV 1 {} {} {}'.format(speed[0], speed[1], speed[2]))
        # this may cause problem,
        # FIXME: Fergus board seems to require read for working properly. 
        ferg_board_ser.readline()
    else:
        pass

    if pressed_key in move_keys.keys():
        if arduino_connect is True:
            ferg_board_ser.write('JOG 1 {} {} {} \r'.format(move_keys[pressed_key][0], move_keys[pressed_key][1], move_keys[pressed_key][2]).encode())
        else: 
            print('JOG 1 {} {} {} \r'.format(move_keys[pressed_key][0], move_keys[pressed_key][1], move_keys[pressed_key][2]).encode())

    elif pressed_key in (']','['): 
        if pressed_key == ']':
            speed = speed*2
        elif pressed_key == '[':
            speed = speed/2
        print('speed: {}'.format(speed))
        if arduino_connect is True:
            ferg_board_ser.write('STV 1 {} {} {}'.format(speed[0], speed[1], speed[2]))
        else: 
            print('STV 1 {} {} {} \r'.format(speed[0], speed[1], speed[2]).encode())
        
    elif pressed_key in ['t']:
        print('start timelapse')

    elif pressed_key in ['x']:
        print('press x again to stop the programme')
    
    else:
        pass


if __name__ == "__main__":
    while True:
        time.sleep(0.2)
        pressed_key = readkey()
        #ferg_board_key_input(arduino_connect=False, pressed_key = pressed_key)
        print('next')
        if pressed_key == 'x':
            break