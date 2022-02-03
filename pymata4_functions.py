import time
import sys
from pymata4 import pymata4

# Setup a pin for analog input and monitor its changes
pin_DI = 7
pin_DO = 13
pin_AI = 2
pin_AO = 12
POLL_TIME = 1  # number of seconds between polls

def analog_in(my_board, pin):
    """
    This function establishes the pin as an analog input. Any changes on this pin will
    be reported through the call back function. Every POLL_TIME seconds, the last value and time
    stamp is polled and printed. Also, the differential parameter is being used.
    The callback will only be called when there is a difference of 10 or more between
    the current and last value reported. Accurate up to the 1st decimal value for 0-5V A.in

    :param my_board: a pymata4 instance
    :param pin: Arduino pin number
    """
    # differential = 10 or 0.05V from (10/1024)*5
    my_board.set_pin_mode_analog_input(pin, callback=callback_AI, differential=5)
    # run forever waiting for input changes
    try:
        while True:
            time.sleep(POLL_TIME)
            # retrieve both the value and time stamp with each poll
            # analog_read returns a tuple of the last value change and the time that it occurred
            value, time_stamp = my_board.analog_read(pin)
            # format the time stamp and value
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))
            formatted_value = (value / 1024) * 5  # converted to voltage
            print(
                f'Reading latest A.in for pin{pin} = {formatted_value:.2f} V '
                f'change received on {formatted_time}')
    except KeyboardInterrupt:
        my_board.shutdown()
        sys.exit(0)
def callback_AI(data):
    """
    A callback function to report data changes.
    :param data: [pin_mode, pin, current_reported_value,  timestamp]
    """
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[3]))
    formatted_data = (data[2] / 1024) * 5  # converted to voltage
    print(f'A.In value change detected: pin{data[1]}, Value = {formatted_data:.2f} Time = {formatted_time}')

def digital_in(my_board, pin):
    """
    This function establishes the pin as a digital input. Any changes on this pin will
    be reported through the call back function.
    :param my_board: a pymata4 instance
    :param pin: Arduino pin number
    """

    # set the pin mode
    my_board.set_pin_mode_digital_input(pin, callback=callback_DI)

    while True:
        try:
            # Do a read of the last value reported every POLL_TIME seconds and print it
            # digital_read returns A tuple of last value change and the time that it occurred
            value, time_stamp = my_board.digital_read(pin)
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))
            print(f'Polling - last value: {value} received on {formatted_time} ')
            time.sleep(POLL_TIME)
        except KeyboardInterrupt:
            board.shutdown()
            sys.exit(0)

def callback_DI(data):
    """
    A callback function to report data changes. This will print the pin number, its reported value and
    the date and time when the change occurred.
    :param data: [pin_mode, pin, current_reported_value, timestamp]
    """
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[3]))
    print(f'Callback DI - Pin: {data[1]} Value: {data[2]} Time Stamp: {formatted_time}')

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
            my_board.digital_pin_write(pin, 1)
            break
        else:
            my_board.digital_pin_write(pin, 0)
            break

if __name__ == '__main__':

    board = pymata4.Pymata4()
    digital_out(board, pin_DO, 1)
    try:
        digital_in(board, pin_DI)

    except KeyboardInterrupt:
        board.shutdown()
        sys.exit(0)
