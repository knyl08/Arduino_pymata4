import sys
import time
from pymata4 import pymata4

"""
This example sets up and control an ADXL345 i2c accelerometer.
It will continuously print data the raw xyz data from the device.
"""

def i2c_current(my_board, mA):
    """
    This function acts as a DAC which uses the PWM digital output as an analog signal.
    User needs to enter % valve opening and the pin outputs the corresponding 0-5V signal.

    :param my_board: an PymataExpress instance
    :param mA: enter the 4-20 mA target value
    """
    my_board.set_pin_mode_i2c()                                 # 4 - 20 mA signal from DAC values of 600 - 3020
    y = int((mA * 151.25)-5)                                    # linear coordinates: (4,600),(20,3020)
    a = y >> 4                                                  # y = mx + b; m = 151.25; b = -5
    b = ((y & 15) << 4)
    my_board.i2c_write(address_c, [64, a, b])
    print("Output: ~{:.2f} mA".format(mA))

def i2c_voltage(my_board, percent):
    """
    This function acts as a DAC which uses the PWM digital output as an analog signal.
    User needs to enter % valve opening and the pin outputs the corresponding 0-5V signal.

    :param my_board: an PymataExpress instance
    :param percent: 0-100% to be converted to 0-10V via i2c line
    """
    my_board.set_pin_mode_i2c()

    i = int((percent / 100) * 4095)
    a = i >> 4
    b = ((i & 15) << 4)
    my_board.i2c_write(address_v, [64, a, b])

    print("Output: ~{:.2f} V".format((percent/100)*10))

def i2c_voltage_user(my_board):
    """
    This function acts as a DAC which uses the PWM digital output as an analog signal.
    User needs to enter % valve opening and the pin outputs the corresponding 0-5V signal.

    :param my_board: an PymataExpress instance
    :param percent: 0-100% to be converted to 0-10V via i2c line
   """

    my_board.set_pin_mode_i2c()

    while True:
        percent = input('Please enter % valve opening from 0-100. Type stop to exit the program.\n ')
        try:
            percent = int(percent)                                          # check if input can be converted to int
        except:                                                             # if not,
            if percent.lower() == "stop":                                   # check if user typed 'stop'
                print('\033[92m' + 'TEST DONE' + '\033[0m')                 # if so,
                board.i2c_write(address_v, [64, 0, 0])                      # turn off i2c 0-10V
                break                                                       # stop the program
            else:                                                           # if user typed other characters
                print("\033[93m" + "Sorry, I didn't understand that." + "\033[0m")
                board.i2c_write(address_v, [64, 0, 0])                      # turn off i2c 0-10V
                continue                                                    # go back to top of while loop
        if int(percent) < 0 or int(percent) > 100:                          # if not within range of 0-100
            print("\033[93m" + "Out of range. Try again. " + "\033[0m")
            board.i2c_write(address_v, [64, 0, 0])                          # turn off i2c 0-10V
            continue                                                        # go back to top of while loop
        else:                                                               # USER INPUT IS GOOD
            i = int((percent / 100) * 4095)                                 # convert 0-100% to 0-4095 DAC value
            a = i >> 4                                                      # ex. 0b11111111, 0b11110000 - binary equivalent of 4095 (5V),
            b = ((i & 15) << 4)                                             # where the last 4 digits (0000) do not matter
            board.i2c_write(address_v, [64, a, b])                          # board.i2c_voltage(address, [write cmd, 0bXXXXXXXX, 0bXXXXXXXX])
            print("Output: ~{:.2f} V".format((percent/100)*10))             # print Vout, 2 decimals
            continue

if __name__ == '__main__':
    address_v = 0x60
    address_c = 0x61
    board = pymata4.Pymata4()
    try:
        i2c_current(board,10)
        board.shutdown()
    except KeyboardInterrupt:
        print("\033[92m" + "TEST DONE" + "\033[0m")
        board.shutdown()
        sys.exit(0)