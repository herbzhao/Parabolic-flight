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
        

    def serial_write(self, serial_command, parser):
        ''' sending the parsed serial_commands'''
        if parser == 'waterscope' or parser == 'ws':
            self.serial_command = self.parsing_command_waterscope(serial_command)
        elif parser == 'fergboard' or parser == 'ferg':
            self.serial_command = self.parsing_command_fergboard(serial_command)
        elif parser == 'parabolic_flight' or parser == 'parabolic':
            self.serial_command = self.parsing_command_parabolic_flight(serial_command)
        else:
            self.serial_command = serial_command

        print(self.serial_command)
        self.ser.write('{} \n\r'.format(str(self.serial_command)).encode())

    def parsing_command_waterscope(self, serial_command):
        ''' parsing the command from interface for WaterScope water testing kit (Sammy code)'''
        # move(distance,speed)
        if 'move' in serial_command:
            serial_command = serial_command.replace('move', 'M')
        # LED_RGB(255,255,255)
        elif 'LED_RGB' in serial_command:
            serial_command = serial_command.replace('LED RGB', 'C')
        # set_temp(30)
        elif 'set_temp':
            serial_command = serial_command.replace('set_temp', 'T')
        elif 'home' in serial_command:
            serial_command = 'H'

        serial_command = serial_command.replace(' ','').replace('(','').replace(')','')
        return serial_command

    def parsing_command_fergboard(self, serial_command):
        ''' parsing the command from interface for fergboard (fergus)'''
        # move(x, y, z)
        if 'move' in serial_command:
            serial_command = serial_command.replace('move', 'MOV')
        # set_speed(x,y,z)
        elif 'set_speed' in serial_command:
            serial_command = serial_command.replace('set_speed', 'STV')
        # jog(x,y,z)
        elif 'jog' in serial_command:
            serial_command = serial_command.replace('jog', 'JOG') 

        serial_command = serial_command.replace('(',' 1 ').replace(')','').replace(",", " ")
        return serial_command

    def parsing_command_parabolic_flight(self, serial_command):
        ''' parsing the command from interface for parabolic flight arduino'''
        serial_command = serial_command.replace(' ','').replace('(','').replace(')','')
        return serial_command

    def serial_read(self, options=['quiet']):
        self.stop_threading = False
        while True:
            # incorporate a flag that stop the thread 
            if self.stop_threading is True:
                break
            else:
                time.sleep(0)
            # only when serial is available to read
            # if ser.in_waiting:
                if self.ser.in_waiting:
                    self.serial_output = self.ser.readline().decode()
                    if options[0] == 'quiet':
                        pass
                    elif options[0] == 'logging':
                        print(self.serial_output)
                        # NOTE: the options[1] is the folder name
                        # if not specified the folder name, use the starting time for the folder name
                        if len(options) == 1:
                            options.append(self.starting_time)
                        # create the folder for the first time.
                        if not os.path.exists("timelapse/{}".format(options[1])):
                            os.mkdir("timelapse/{}".format(options[1]))
                        log_file_location = "timelapse/{}/temp_log.txt".format(options[1])
                        with open(log_file_location, 'a+') as log_file:
                            log_file.writelines(self.serial_output)
                    else:
                        print(self.serial_output)


                

    def serial_read_threading(self, options=['quiet']):
        ''' used to start threading for reading the serial'''
        # now threading1 runs regardless of user input
        self.threading_ser_read = threading.Thread(target=self.serial_read, args=[options])
        self.threading_ser_read.daemon = True
        self.threading_ser_read.start()
        time.sleep(2)

    def close(self):
        # TODO: add a way to shut the thread, possibly by passing a flag to each loop
        self.stop_threading = True
        time.sleep(0.2)
        self.ser.close()

#############################################
# code starts here
if __name__ == '__main__':
    serial_controller = serial_controller_class()
    serial_controller.serial_connect(port_names=['SERIAL'], baudrate=9600)
    #serial_controller.serial_connect(port_names=['Micro'], baudrate=115200)
    serial_controller.serial_read_threading(options='logging')

    # accept user input
    while True:
        user_input = str(input())
        serial_controller.serial_write(user_input, 'fergboard')
            
