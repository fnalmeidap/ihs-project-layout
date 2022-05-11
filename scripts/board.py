#!/usr/bin/python3

# PLACA 02

import os, sys
from fcntl import ioctl
from ioctl_cmds import *

if len(sys.argv) < 2:
    print("Error: expected more command line arguments")
    print("Syntax: %s </dev/device_file>"%sys.argv[0])
    exit(1)

fd = os.open(sys.argv[1], os.O_RDWR)

class DE2i:
    def __init__(self, file) -> None:
        self.__file = file
        self.__c_state = {
            "left_display": 0x0,
            "right_display": 0x0,
            "switches": 0x0,
            "push_buttons": 0x0,
            "red_led": 0x0,
            "green_led": 0x0,
        }
        self.__hex_map = {
            0:0x40,
            1:0x79,
            2:0x24,
            3:0x30,
            4:0x19,
            5:0x12,
            6:0x2,
            7:0x78,
            8:0x0,
            9:0x10
        }
    
    def set_display(self, side = "", d1 = 0, d2 = 0, d3 = 0, d4 = 0):
        first = self.__hex_map[d1]
        second = self.__hex_map[d2]
        third = self.__hex_map[d3]
        fourth = self.__hex_map[d4]

        current_value = 0
        
        # alter the first 7-seg-display
        current_value = first << 24 | current_value
        
        # alter the second 7-seg-display
        current_value = second << 16 | current_value

        # alter the third 7-seg-display
        current_value = third << 8 | current_value

        # alter the fourth 7-seg-display
        current_value = fourth | current_value

        if side == "left":
            ioctl(fd, WR_L_DISPLAY)
            retval = os.write(self.__file, current_value.to_bytes(4, 'little'))
            print("wrote %d bytes"%retval)
        elif side == "right":
            ioctl(fd, WR_R_DISPLAY)
            retval = os.write(self.__file, current_value.to_bytes(4, 'little'))
            print("wrote %d bytes"%retval)
        else:
            raise "Invalid side"

        self.__c_state[f'{side}_display'] = current_value

    def set_red_led(self, leds_dict): 
        setting = 0x0

        for bit_position, value in leds_dict
            if value == 0:
                setting = mask << bit_position & 0
            elif value == 1:
                setting = mask << bit_position | 1

        ioctl(fd, WR_RED_LEDS)
        retval = os.write(fd, setting.to_bytes(4, 'little'))
        print("wrote %d bytes"%retval)

    def set_green_led(self):
        raise NotImplementedError

    def get_pbuttons(self):
        raise NotImplementedError
    
    def get_switches(self):
        raise NotImplementedError   
    


board = DE2i(fd)
board.set_display(side ="left", d1 = 1, d2 = 1, d3 = 1, d4 = 1)

leds_dict = { 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0 }
board.set_red_led(leds_dict)

ioctl(fd, RD_PBUTTONS)
red = os.read(fd, 4); # read 4 bytes and store in red var
print("red 0x%X"%int.from_bytes(red, 'little'))

os.close(fd)
