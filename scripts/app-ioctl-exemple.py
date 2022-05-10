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

def write_on_display(current_value, first = 0, second = 0, third = 0, fourth = 0):
    hex_map = {
        0:0x40,
        1:0x79,
        2:0xFFFFFFA4,
        3:0x30,
        4:0x19,
        5:0x12,
        6:0x2,
        7:0x78,
        8:0x0,
        9:0x10
    }
    
    first = hex_map[first]
    second = hex_map[second]
    third = hex_map[third]
    fourth = hex_map[fourth]
    
    # alter the first 7-seg-display
    current_value = first << 24 | (data & 0xFFFFFF)

    return current_value

# data to write
# utl = 0x24

data = 0x40404079
data = write_on_display(data, first=5)
# data = utl << 24 | (data & 0xFFFFFF)

ioctl(fd, WR_R_DISPLAY)
retval = os.write(fd, data.to_bytes(4, 'little'))
print("wrote %d bytes"%retval)

# data to write
data = 0x79404040

ioctl(fd, WR_L_DISPLAY)
retval = os.write(fd, data.to_bytes(4, 'little'))
print("wrote %d bytes"%retval)

ioctl(fd, RD_PBUTTONS)
red = os.read(fd, 4); # read 4 bytes and store in red var
print("red 0x%X"%int.from_bytes(red, 'little'))

os.close(fd)
