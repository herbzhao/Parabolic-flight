from readchar import readkey
import serial
import serial.tools.list_ports
import numpy as np
import time
import threading

from serial_communication import serial_controller_class

class arduino_controller_class():
    def __init__(self, fergboard_connect=False, arduino_connect=False, waterscope_connect=False):
        # some parameters
        self.move_keys = {
            'w': [0,-1,0],
            's': [0,1,0],
            'a': [-1,0,0],
            'd': [1,0,0],
            'q': [0,0,1],
            'e': [0,0,-1]
                    }
        self.fergboard_speed = np.array([200, 200, 200])
        self.fergboard_connect = fergboard_connect
        self.arduino_connect = arduino_connect
        self.waterscope_connect = waterscope_connect
        # later on save it to a YAML
        self.serial_controllers_settings = {
            'waterscope' : {'port_names' : ['ws'], 'baudrate': 9600, 'serial_read_options': ['quiet']},
            'ferg': {'port_names' : ['Micro'], 'baudrate': 115200, 'serial_read_options': ['quiet']},
            # Change: the folder name for serial_read_options[1]
            'para': {'port_names' : ['SERIAL'], 'baudrate': 9600, 'serial_read_options': ['logging', 'heatmass_PID']},
        }
        self.initialse_serial_connection()
    
    def initialse_serial_connection(self):
        # to store the names for the arduinos that want to be connected
        serial_controllers_names = []
        # create an empty dict to store all the serial_controller_class
        self.serial_controllers = {}

        if self.fergboard_connect is True:
            serial_controllers_names.append('ferg')
        if self.arduino_connect is True:
            serial_controllers_names.append('para')
        if self.waterscope_connect is True:
            serial_controllers_names.append('waterscope')

        # initialise the connection with existing arduinos using the settings in the dictionary
        for name in serial_controllers_names:
            self.serial_controllers[name] = serial_controller_class()
            self.serial_controllers[name].serial_connect(
                port_names=self.serial_controllers_settings[name]['port_names'], 
                baudrate=self.serial_controllers_settings[name]['baudrate'])
            self.serial_controllers[name].serial_read_threading(options=self.serial_controllers_settings[name]['serial_read_options'])

    def key_input(self):
        # initialise fergboard speed
        if self.fergboard_connect is True:
            serial_command = 'set_speed ({}, {}, {})'.format(self.fergboard_speed[0], self.fergboard_speed[1], self.fergboard_speed[2])
            self.serial_controllers['ferg'].serial_write(serial_command, parser='fergboard')
            print('reading keys')

        while True:
            # read keyboard input (from SSH or from Raspberry Pi)
            k = readkey()

            if k in self.move_keys.keys():
                ''' Motor movement'''
                serial_command = 'jog({},{},{})'.format(self.move_keys[k][0], self.move_keys[k][1], self.move_keys[k][2])
                if self.fergboard_connect is True:
                    self.serial_controllers['ferg'].serial_write(serial_command, parser='fergboard')
                    # wait for the movement to finish
                    while True:
                        if 'FIN' in self.serial_controllers['ferg'].serial_output:
                            # as this will no longer update, assign a new empty value 
                            # TODO: is this necessary actually???
                            self.serial_controllers['ferg'].serial_output = ''
                            break
                        time.sleep(0.1)
                elif self.fergboard_connect is False:
                    print(serial_command)

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
                serial_command = 'set_speed ({}, {}, {})'.format(self.fergboard_speed[0], self.fergboard_speed[1], self.fergboard_speed[2])

                # send command to adjust speed
                if self.fergboard_connect is True:
                    self.serial_controllers['ferg'].serial_write(serial_command, parser='fergboard')
                elif self.fergboard_connect is False:
                    print(serial_command)

            # arduino connection for temperature control
            elif k in ['v', 'b']:
                ''' peltier controlling'''
                if k == 'v':
                    print('start cooling')
                    serial_command = 'cool'
                    if self.arduino_connect is True:
                        self.serial_controllers['para'].serial_write(serial_command, parser='parabolic_flight')
                        pass
                if k == 'b':
                    print('start heating')
                    serial_command = 'heat'
                    if self.arduino_connect is True:
                        self.serial_controllers['para'].serial_write(serial_command, parser='parabolic_flight')
            elif k in ['x']:
                print('Exiting...')
                if self.fergboard_connect is True:
                    self.serial_controllers['ferg'].close()
                if self.arduino_connect is True:
                    self.serial_controllers['para'].close()
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
        