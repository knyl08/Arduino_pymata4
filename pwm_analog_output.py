import sys
from pymata4 import pymata4

"""
Setup a pin for PWM (aka analog) output 0-5 V.
"""
pin_AO = 5

def analog_out(my_board, pin):
    """
    This function acts as a DAC which uses the PWM digital output as an analog signal.
    User needs to enter % valve opening and the pin outputs the corresponding 0-5V signal.

    :param my_board: an PymataExpress instance
    :param pin: pin to be controlled
    TODO: Add a percent parameter. If provided, proceed to output the PWM
        based on the given parameter. If not, ask user to enter the %.
    """
    my_board.set_pin_mode_pwm_output(pin)

    while True:
        percent = input('Please enter % valve opening from 0-100. Type stop to exit the program.\n ')
        try:
            percent = int(percent)                                          # check if input can be converted to int
        except:                                                             # if not,
            if percent.lower() == "stop":                                   # check if user typed 'stop'
                print('\033[92m' + 'TEST DONE' + '\033[0m')                 # if so,
                break                                                       # stop the program
            else:                                                           # if user typed other characters
                print("\033[93m" + "Sorry, I didn't understand that." + "\033[0m")
                continue                                                    # go back to top of while loop
        if int(percent) < 0 or int(percent) > 100:                          # if not within range of 0-100
            print("\033[93m" + "Out of range. Try again. " + "\033[0m")
            continue                                                        # go back to top of while loop
        else:                                                               # we're happy with the input
            pwm = int( (percent / 100) * 255 )
            my_board.pwm_write(pin, pwm)                                    # output 0-5V a.signal
            print("Output: ~{:.2f} V".format((percent/100)*5))              # print only 2 decimals
            continue

if __name__ == '__main__':
    board = pymata4.Pymata4()
    try:
        analog_out(board, pin_AO)
        board.shutdown()
    except KeyboardInterrupt:
        print("\033[92m" + "TEST DONE" + "\033[0m")
        board.shutdown()
        sys.exit(0)


