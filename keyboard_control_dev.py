from readchar import readkey
import serial
import serial.tools.list_ports
import numpy as np
import time
import threading

from serial_communication import serial_controller_class

class arduino_controller_class():
    def __init__(self, fergboard_connect=False, arduino_connect=False):
        # some parameters
        self.move_keys = {
            'w': [0,1,0],
            's': [0,-1,0],
            'a': [1,0,0],
            'd': [-1,0,0],
            'q': [0,0,-1],
            'e': [0,0,1]
                    }
        self.fergboard_speed = np.array([200, 200, 200])
        self.fergboard_connect = fergboard_connect
        self.arduino_connect = arduino_connect
        if self.fergboard_connect is True:
            self.initialise_fergboard_connection()
        if self.arduino_connect is True:
            self.initialise_arduino_connection()
        
    def initialise_fergboard_connection(self):
        self.ferg_ser_contoller = serial_controller_class()
        self.ferg_ser_contoller.serial_connect(port_names=['Micro'], baudrate=115200)
        self.ferg_ser_contoller.serial_read_threading(option='quiet')


    def initialise_arduino_connection(self):
        self.arduino_ser_contoller = serial_controller_class()
        self.arduino_ser_contoller.serial_connect(port_names=['SERIAL'], baudrate=9600)
        # change the folder name here
        self.arduino_ser_contoller.serial_read_threading(option='logging', folder_name='CE0.8')


    def key_input(self):
        # initialise fergboard speed
        if self.fergboard_connect is True:
            self.ferg_ser_contoller.parsing_command_fergboard('set_speed ({}, {}, {})'.format(self.fergboard_speed[0], self.fergboard_speed[1], self.fergboard_speed[2]))
            self.ferg_ser_contoller.serial_write()
            print('reading keys')

        while True:
            # read keyboard input (from SSH or from Raspberry Pi)
            k = readkey()

            if k in self.move_keys.keys():
                ''' Motor movement'''
                if self.fergboard_connect is True:
                    self.ferg_ser_contoller.parsing_command_fergboard('jog({},{},{})'.format(self.move_keys[k][0], self.move_keys[k][1], self.move_keys[k][2]))
                    self.ferg_ser_contoller.serial_write()

                    # wait for the movement to finish
                    while True:
                        if 'FIN' in self.ferg_ser_contoller.serial_output:
                            self.ferg_ser_contoller.serial_output = ''
                            break
                        time.sleep(0.01)
                        
                else: 
                    print('jog({},{},{})'.format(self.move_keys[k][0], self.move_keys[k][1], self.move_keys[k][2]))


            elif k in (']','['): 
                ''' Motor speed control'''
                if k == ']':
                    self.fergboard_speed = self.fergboard_speed+100
                elif k == '[':
                    self.fergboard_speed = self.fergboard_speed-100
                # limit the speed  between 50 and 500
                if self.fergboard_speed[0] > 500:
                    self.fergboard_speed = np.array([600,600,600])
                elif self.fergboard_speed[0] < 50:
                    self.fergboard_speed = np.array([100,100,100])
                # the speed has to be integer
                self.fergboard_speed = self.fergboard_speed.astype('int')
                print('speed: {}'.format(self.fergboard_speed))
                # send command to adjust speed
                if self.fergboard_connect is True:
                    self.ferg_ser_contoller.parsing_command_fergboard('set_speed ({}, {}, {})'.format(self.fergboard_speed[0], self.fergboard_speed[1], self.fergboard_speed[2]))
                    self.ferg_ser_contoller.serial_write()
                else: 
                    print('set_speed ({}, {}, {})'.format(self.fergboard_speed[0], self.fergboard_speed[1], self.fergboard_speed[2]))

            # arduino connection for temperature control
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
                if self.fergboard_connect is True:
                    self.ferg_ser_contoller.close()
                if self.arduino_connect is True:
                    self.arduino_ser_contoller.close()
                break


if __name__ == "__main__":
    # now threading0 runs regardless of user input
    arduino_controller = arduino_controller_class(fergboard_connect=False, arduino_connect=True)
    threading_keyinput = threading.Thread(target=arduino_controller.key_input())
    threading_keyinput.daemon = True
    threading_keyinput.start()


    # running the program continuously
    while True:
        if not threading_keyinput.isAlive():
            break
        