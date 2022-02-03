import sys
import time
from pymata4 import pymata4

"""
Setup a pin for PWM (aka analog) output and output
some different values.
"""

def set_intensity(my_board, pin):
    """
    This function will set an LED and set it to
    several PWM intensities.
    :param my_board: an PymataExpress instance
    :param pin: pin to be controlled
    """

    # set the pin mode
    print('pwm_analog_output example')
    my_board.set_pin_mode_pwm_output(pin)

    # set the intensities with analog_write
    print('Maximum Intensity')
    my_board.pwm_write(pin, 255)
    time.sleep(5)
    print('Mid Range Intensity')
    my_board.pwm_write(pin, 128)
    time.sleep(5)
    print('Off')
    my_board.pwm_write(pin, 0)


board = pymata4.Pymata4()
set_intensity(board, 13)

# here we clean up after the program completes.
board.shutdown()
sys.exit(0)