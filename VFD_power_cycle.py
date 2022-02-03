import sys
import time
from datetime import datetime
from pymata4 import pymata4

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
def digital_in(my_board, pin):
    """
    This function establishes the pin as a digital input. Any changes on this pin will
    be reported through the call back function.
    :param my_board: a pymata4 instance
    :param pin: Arduino pin number
    """

    # set the pin mode
    # my_board.set_pin_mode_digital_input(pin, callback=callback_DI)
    my_board.set_pin_mode_digital_input(pin)

    while True:
        try:
            # Do a read of the last value reported every POLL_TIME seconds and print it
            # digital_read returns a tuple of last value change and the time that it occurred
            value, time_stamp = my_board.digital_read(pin)
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))
            print(f'VFD power state: {value} received on {formatted_time} ')
            time.sleep(1)
            return value

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

if __name__ == '__main__':

    # Added checking of failure. Check if VFD is ON (via variable vfd_on 1/0)
    # when supposed to be on and OFF when it is supposed to be off.
    # TODO:  Failure count is working when VFD fails to turn on. Code continues to try to turn it ON.
    #   Needs improvement when VFD fails to turn off. Code does not proceed with the code and relay stays off.

    board = pymata4.Pymata4()
    relay_pin = 2
    vfd_on = 7 # DI7 wired from 24V DEPC supply (converted to 5V) for VFD power status
    t_on = 10
    t_off = 5

    digital_out(board, relay_pin, 0) # Initialize pin, Active-high, Relay OFF
    digital_out(board, 13, 1) # 5V to be used as signal for DI7

    count = 0
    fail = 0

    try:
        while True:
            # Check that DI7 is LOW, VFD is OFF, then go to Turn ON mains
            # If DI7 is high, prompt user to turn off mains
            value = digital_in(board,vfd_on) #read DI
            if value == 1:
                fail = fail + 1
                print(f'VFD is still on. Please power down. Failure count = {fail}')
                digital_out(board, relay_pin, 0)  # Turn off relay
                pass
            else:
                # Turn ON mains
                digital_out(board, relay_pin, 1)
                dateTimeObj = datetime.now()
                timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")
                print("\033[42m","Relay ON"," \033[0m", timestampStr)
                #Countdown in seconds
                for remaining in range(t_on, 0, -1):
                    sys.stdout.write("\r")
                    sys.stdout.write("{:2d} second/s remaining.".format(remaining))
                    sys.stdout.flush()
                    time.sleep(1)
                sys.stdout.write("\r                     \n")

            # Check that DI7 is HIGH, VFD ON, then go to Turn OFF mains
            # If DI7 is LOW, prompt user that VFD was not able to turn on on last cycle
            value = digital_in(board, vfd_on)
            if value == 0:
                fail = fail + 1
                print(f'VFD is still OFF. Proceeding to next cycle. Failure count = {fail}')
                digital_out(board, relay_pin, 0)  # Turn off relay
                time.sleep(t_off)
                pass
            else:
                # Turn OFF mains
                digital_out(board, relay_pin, 0)
                dateTimeObj = datetime.now()
                timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")
                count = count + 1
                print("\033[37m","Relay OFF","\033[0m", timestampStr, ":: count = ", count, ":: fail = ", fail)

                # Countdown in seconds
                for remaining in range(t_off, 0, -1):
                    sys.stdout.write("\r")
                    sys.stdout.write("{:2d} second/s remaining.".format(remaining))
                    sys.stdout.flush()
                    time.sleep(1)
                sys.stdout.write("\r                     \n")

    except KeyboardInterrupt:
        digital_out(board, relay_pin, 0) #Turn off relay
        print("\n","\033[92m","TEST DONE","\033[0m")
        board.shutdown()
        sys.exit(0)