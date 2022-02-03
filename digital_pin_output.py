import sys
import time
from pymata4 import pymata4

"""
Setup a pin for digital output and output
and toggle the pin using the digital_pin_output as opposed to digital_output
pin mode.
"""


def digital_out(my_board, pin, state):
    """
    This function will toggle a digital pin.

    :param my_board: an PymataExpress instance
    :param pin: pin to be controlled
    :param state: 1 for ON, else OFF, i.e. 0 or otherwise
    """

    # set the pin mode
    my_board.set_pin_mode_digital_output(pin)

    while True:
        if state == 1:
            print("\033[42m" + " Relay ON " + "\033[0m")
            time.sleep(0.5)
            my_board.digital_pin_write(pin, 1)
            break
        else:
            print("\033[37m" + " Relay OFF " + "\033[0m")
            time.sleep(0.5)
            my_board.digital_pin_write(pin, 0)
            break

if __name__ == '__main__':
    board = pymata4.Pymata4()
    try:
        digital_out(board, 2, 1)
        time.sleep(3)
        digital_out(board, 2, 0)
        time.sleep(1)
        digital_out(board, 2, 1)
        time.sleep(3)
        digital_out(board, 2, "sdf")
        time.sleep(1)
        board.shutdown()
    except KeyboardInterrupt:
        print("\033[92m" + "TEST DONE" + "\033[0m")
        board.shutdown()
        sys.exit(0)

