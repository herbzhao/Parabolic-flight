def parsing_command_waterscope(command):
    ''' parsing the command from interface to serial_command'''
    # move(distance,speed)
    if 'move' in command:
        print('move in command')
        command.replace('move', 'M')
    # LED_RGB(255,255,255)
    elif 'LED_RGB' in command:
        command.replace('LED RGB', 'C')
    # set_temp(30)
    elif 'set_temp':
        command.replace('set_temp', 'T')
    elif 'home' in command:
        command = 'H'

    command.replace(' ','').replace('(','').replace(')','')
    print(command)
    serial_command = command


while True:
    user_input = input()
    user_input.replace('move', 'M')
    print(user_input)


    if user_input == 'x':
        break
