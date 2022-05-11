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
        setting = 0

        for bit_position, value in leds_dict.items():
            if value == 0:
                setting = ~(1 << bit_position) & setting
            elif value == 1:
                setting = 1 << bit_position | setting

        ioctl(fd, WR_RED_LEDS)
        retval = os.write(fd, setting.to_bytes(4, 'little'))
        print("wrote %d bytes"%retval)


    def set_green_led(self, leds_dict):
        setting = 0
        
        for bit_position, value in leds_dict.items():
            if value == 0:
                setting = ~(1 <<  bit_position) & setting
            elif value == 1:
                setting = 1 << bit_position | setting
        
        ioctl(fd, WR_GREEN_LEDS)
        retval = os.write(fd, setting.to_bytes(4, 'little'))
        print("wrote %d bytes"%retval)


    def get_pbuttons(self):
        ioctl(fd, RD_PBUTTONS)
        c_setting = os.read(fd,4)
        c_setting = int.from_bytes(c_setting, 'little')
        print(c_setting)

        push_buttons = [0, 0, 0, 0]

        for bit_position in range(0, 4):
            if ((1 << bit_position) & c_setting) == 1:
                push_buttons[bit_position] = True # apertado
            else:
                push_buttons[bit_position] = False # não apertado

        print(push_buttons)
    
    def get_switches(self):
        raise NotImplementedError   
    


board = DE2i(fd)
board.set_display(side ="left", d1 = 1, d2 = 1, d3 = 1, d4 = 1)

red_leds_dict = { 0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:1 }
board.set_red_led(red_leds_dict)

green_leds_dict = { 0:1, 1:0, 2:1, 3:0, 4:0, 5:0, 6:0, 7:1, 8:1 }
board.set_green_led(green_leds_dict)

board.get_pbuttons()

os.close(fd)
