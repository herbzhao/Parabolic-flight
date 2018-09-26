import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Change here
folder_name = 'timelapse/CE0.8/'
file_name = 'CE_0.8_'

with open(folder_name+'temp_log.txt', 'r+') as temp_log_file:
    temp_log_content = temp_log_file.read()
    # remove the blank lines
    temp_log_content = temp_log_content.replace('\n\n','\n')
    temp_log_content = temp_log_content.split('\n')

    # log_seconds = [float(value.replace(' s', '')) for i, value in enumerate(temp_log_content) if i%2 == 0]
    # log_temperature = [float(value.replace(' *C','')) for i, value in enumerate(temp_log_content) if i%2 == 1]
    # print(log_temperature)

    seconds_log = []
    temperature_log = []

    for i, value in enumerate(temp_log_content):
        if i%2 == 0:
            try:
                # print(value)
                seconds_log.append(float(value.replace(' s', '')))
            except ValueError:
                pass
        else:
            try:
                # print(value)
                temperature_log.append(float(value.replace(' *C','')))
            except ValueError:
                pass

    # convert everything to numpy float for easy plotting
    temperature_log = np.array(temperature_log)
    # trim off the last log_seconds because it is empty
    seconds_log = np.array(seconds_log)
    print(len(temperature_log))
    print(len(seconds_log))
    
    temp_log_content = {'temperature (C)': temperature_log, 'time (s)': seconds_log}

    # save as CSV
    df = pd.DataFrame(temp_log_content).set_index('time (s)')
    df.to_csv(folder_name+file_name+'log.csv')
    df.plot.line()
    plt.show()