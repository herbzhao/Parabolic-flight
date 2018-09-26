from __future__ import division

import threading
import serial.tools.list_ports
import serial
import time
import datetime
import os


class serial_controller_class():
    def __init__(self):
        self.starting_time = time.time()
        self.serial_output = ''
        self.starting_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    def time_logger(self):
        self.time_elapsed = '{:.1f}'.format(time.time() - self.starting_time)


    def serial_connect(self, port_names=['SERIAL'], baudrate=9600 ):
        ''' automatically detect the Ardunio port and connect '''
        # Find Arduino serial port first
        available_ports = list(serial.tools.list_ports.comports())
        for port in available_ports:
            for name in port_names:
                if name in port[1]:
                    serial_port = port[0]
                    print('Serial port: '+ serial_port)


        self.ser = serial.Serial()
        self.ser.port = serial_port
        self.ser.baudrate = baudrate
        # TODO: check the meaning of the time out
        # self.ser.timeout = 0
        self.ser.open()
        

    def serial_write(self):
        ''' purly sending the serial information to arduino, the parsing is done in other methods '''
        self.ser.write('{} \n\r'.format(str(self.serial_command)).encode())

    def parsing_command_waterscope(self, command):
        ''' parsing the command from interface for WaterScope water testing kit (Sammy code)'''
        # move(distance,speed)
        if 'move' in command:
            command = command.replace('move', 'M')
        # LED_RGB(255,255,255)
        elif 'LED_RGB' in command:
            command = command.replace('LED RGB', 'C')
        # set_temp(30)
        elif 'set_temp':
            command = command.replace('set_temp', 'T')
        elif 'home' in command:
            command = 'H'

        command = command.replace(' ','').replace('(','').replace(')','')
        print(command)
        self.serial_command = command

    def parsing_command_fergboard(self, command):
        ''' parsing the command from interface for fergboard (fergus)'''
        # move(distance,speed)
        if 'move' in command:
            command = command.replace('move', 'MOV')
        elif 'set_speed' in command:
            command = command.replace('set_speed', 'STV')
        elif 'jog' in command:
            command = command.replace('jog', 'JOG') 

        command = command.replace('(',' 1 ').replace(')','').replace(",", " ")
        print(command)
        self.serial_command = command

    def serial_read(self):
        while True:
        # only when serial is available to read
        # if ser.in_waiting:
            if self.ser.in_waiting:
                self.serial_output = self.ser.readline().decode()
                print(self.serial_output)
    
    def serial_read_quiet(self):
        ''' read the serial output but not print it ''' 
        while True:
        # only when serial is available to read
        # if ser.in_waiting:
            if self.ser.in_waiting:
                self.serial_output = self.ser.readline().decode()

    def serial_read_logging(self, folder_name=''):
        ''' read the serial output and log in a file for further analysis ''' 
        while True:
        # only when serial is available to read
        # if ser.in_waiting:
            if self.ser.in_waiting:
                self.serial_output = self.ser.readline().decode()
                print(self.serial_output)
                # if not specified the folder name, use the starting time for the folder name
                if folder_name == '':
                    folder_name = self.starting_time
                # create the folder for the first time.
                if not os.path.exists("timelapse/{}".format(folder_name)):
                    os.mkdir("timelapse/{}".format(folder_name))
                log_file_location = "timelapse/{}/temp_log.txt".format(folder_name)
                with open(log_file_location, 'a+') as log_file:
                    log_file.writelines(self.serial_output)

    
    def serial_read_threading(self, option='quiet', folder_name=''):
        ''' used to start threading for '''
        if option == 'quiet':
            # now threading1 runs regardless of user input
            self.threading_ser_read = threading.Thread(target=self.serial_read_quiet)
        elif option == 'logging':
            self.threading_ser_read = threading.Thread(target=self.serial_read_logging, args=[folder_name])
        else:
            self.threading_ser_read = threading.Thread(target=self.serial_read)

        self.threading_ser_read.daemon = True
        self.threading_ser_read.start()
        time.sleep(2)

    def close(self):
        self.ser.close()

#############################################
# code starts here
if __name__ == '__main__':
    serial_controller = serial_controller_class()
    serial_controller.serial_connect(port_names=['SERIAL'], baudrate=9600)
    #serial_controller.serial_connect(port_names=['Micro'], baudrate=115200)
    serial_controller.serial_read_threading(option='logging')

    # accept user input
    while True:
        user_input = str(input())
        #serial_controller.parsing_command_waterscope(user_input)
        serial_controller.parsing_command_fergboard(user_input)
        serial_controller.serial_write()

            
