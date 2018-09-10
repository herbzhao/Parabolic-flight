"""Simple example showing how to get gamepad events."""

from __future__ import print_function
import threading
from readchar import readkey


def read_keys():
    """Just print out some event infomation when the gamepad is used."""
    while True:
        #events = get_gamepad()
        events = get_key()
        for event in events:
            print(event.ev_type, event.code, event.state)


if __name__ == "__main__":
    # now threading1 runs regardless of user input
    threading1 = threading.Thread(target=read_keys)
    threading1.daemon = True
    threading1.start()

    while True:
        #print('type the distance whenever you want')
        # python 2.7 raw_input
        user_input = str(input())
        if user_input == 'tl':
            print('tl')
        else:
            print('nope')
#
#    main()