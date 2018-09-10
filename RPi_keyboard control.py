from readchar import readkey
import serial
import numpy as np
import time
import threading


class arduino_controller_class():
    def __init__(self, fergboard_connect=False, arduino_connect=False):
        # some parameters
        self.move_keys = {'w': [0,1,0],
                    'a': [1,0,0],
                    's': [0,-1,0],
                    'd': [-1,0,0],
                    'q': [0,0,-1],
                    'e': [0,0,1]}
        self.fergboard_speed = np.array([200, 200, 200])
        self.fergboard_connect = fergboard_connect
        self.arduino_connect = arduino_connect
        if self.fergboard_connect is True:
            self.initialise_fergboard_connection()
        if self.arduino_connect is True:
            self.initialise_arduino_connection()
        
    def initialise_fergboard_connection(self):
        # initialisation the arduino connection
        self.ferg_ser = serial.Serial()
        self.ferg_ser.baudrate = 115200
        self.ferg_ser.timeout = 5
        self.ferg_ser.port = '/dev/ttyACM0'
        self.ferg_ser.open()
        self.ferg_ser.flush()
        # change speed
        self.ferg_ser.write('STV 1 {} {} {}'.format(self.fergboard_speed[0], self.fergboard_speed[1], self.fergboard_speed[2]))
        self.ferg_ser.readline()
        
    def initialise_arduino_connection(self):
        # initialisation the arduino connection
        self.arduino_ser = serial.Serial()
        self.arduino_ser.baudrate = 115200
        self.arduino_ser.timeout = 5
        # TODO: change this to the arduino port
        self.arduino_ser.port = '/dev/ttyACM0'
        self.arduino_ser.open()
        self.arduino_ser.flush()

    def key_input(self):
        # initialise some parameters
        while True:

            # maximum 1 command per 0.5 sec  
            time.sleep(0.5)
            ''' constantly reading the serial output from Fergboard '''
            if self.fergboard_connect is True:
                self.ferg_ser.readline()

            # read keyboard input (from SSH or from Raspberry Pi)
            k = readkey()

            if k in self.move_keys.keys():
                ''' Motor movement'''
                if self.fergboard_connect is True:
                    self.ferg_ser.write('JOG 1 {} {} {} \r'.format(self.move_keys[k][0], self.move_keys[k][1], self.move_keys[k][2]).encode())
                else: 
                    print('JOG 1 {} {} {} \r'.format(self.move_keys[k][0], self.move_keys[k][1], self.move_keys[k][2]).encode())

            elif k in (']','['): 
                ''' Motor speed control'''
                if k == ']':
                    self.fergboard_speed = self.fergboard_speed*2
                elif k == '[':
                    self.fergboard_speed = self.fergboard_speed/2
                print('speed: {}'.format(self.fergboard_speed))
                if self.fergboard_connect is True:
                    self.ferg_ser.write('STV 1 {} {} {}'.format(self.fergboard_speed[0], self.fergboard_speed[1], self.fergboard_speed[2]))
                else: 
                    print('STV 1 {} {} {} \r'.format(self.fergboard_speed[0], self.fergboard_speed[1], self.fergboard_speed[2]).encode())


            elif k in ['v', 'b', 'n', 'm']:
                ''' peltier controlling'''
                if k == 'v':
                    print('start cooling')
                    if self.arduino_connect is True:
                        pass
                if k == 'b':
                    print('stop cooling')
                    if self.arduino_connect is True:
                        pass
                if k == 'n':
                    print('cooling effort increase')
                    if self.arduino_connect is True:
                        pass
                elif k == 'm':
                    print('cooling effort decrease')
                    if self.arduino_connect is True:
                        pass

            elif k in ['x']:
                print('Exiting...')
                break
        
    def read_temperature(self):
        while True:
            #  1 reading per 0.5 sec  -- need to synchronise with arduino output
            time.sleep(0.5)
            print('Temperature: ')
            if self.arduino_connect is True:
                print(self.arduino_ser.readline())

if __name__ == "__main__":
    # now threading0 runs regardless of user input
    arduino_controller = arduino_controller_class(False)
    # the read temperature has to be the first one!
    threading0 = threading.Thread(target=arduino_controller.read_temperature)
    threading0.daemon = True
    threading0.start()

    threading1 = threading.Thread(target=arduino_controller.key_input())
    threading1.daemon = True
    threading1.start()


    # running the program continuously
    while True:
        if not threading1.isAlive():
            break
        