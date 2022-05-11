#!/usr/bin/python3

# PLACA 02

import os, sys
from fcntl import ioctl

RD_SWITCHES = 24929
RD_PBUTTONS = 24930
WR_L_DISPLAY = 24931
WR_R_DISPLAY = 24932
WR_RED_LEDS = 24933
WR_GREEN_LEDS = 24934

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
            ioctl(self.__file, WR_L_DISPLAY)
            retval = os.write(self.__file, current_value.to_bytes(4, 'little'))
            print("wrote %d bytes"%retval)
        elif side == "right":
            ioctl(self.__file, WR_R_DISPLAY)
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

        ioctl(self.__file, WR_RED_LEDS)
        retval = os.write(self.__file, setting.to_bytes(4, 'little'))
        print("wrote %d bytes"%retval)


    def set_green_led(self, leds_dict):
        setting = 0
        
        for bit_position, value in leds_dict.items():
            if value == 0:
                setting = ~(1 <<  bit_position) & setting
            elif value == 1:
                setting = 1 << bit_position | setting
        
        ioctl(self.__file, WR_GREEN_LEDS)
        retval = os.write(self.__file, setting.to_bytes(4, 'little'))
        print("wrote %d bytes"%retval)


    def get_pbuttons(self):
        ioctl(self.__file, RD_PBUTTONS)
        c_setting = os.read(self.__file,4)
        c_setting = int.from_bytes(c_setting, 'little')

        push_buttons = [0, 0, 0, 0]

        for bit_position in range(0, 4):
            if ((1 << bit_position) & c_setting) > 0:
                push_buttons[3 - bit_position] = False # não apertado
            else:
                push_buttons[3 - bit_position] = True # apertado

        print("Push buttons:", push_buttons)
    

    def get_switches(self):
        ioctl(self.__file, RD_SWITCHES)
        c_setting = os.read(self.__file, 4)
        c_setting = int.from_bytes(c_setting, 'little')

        switches = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

        for bit_position in range(0, 18):
            if ((1 << bit_position) & c_setting) > 0:
                switches[17 - bit_position] = True # para cima
            else:
                switches[17 - bit_position] = False # para baixo

        print("Switches:", switches)
