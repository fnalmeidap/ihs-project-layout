import os, sys
from fcntl import ioctl
from scripts.board import DE2i

fd = os.open("/dev/mydev", os.O_RDWR)

################################## BOARD SETUP ##################################

displays = {"side":"right", "d1": 1, "d2":1, "d3":9, "d4": 9}
red_leds_dict = { 0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:1 }
green_leds_dict = { 0:1, 1:0, 2:1, 3:0, 4:0, 5:0, 6:0, 7:1, 8:1 }

################################## BOARD CONTROL ##################################

board = DE2i(fd)

board.set_display("right", d1 = displays["d1"], d2 = displays["d2"], d3 = displays["d3"], d4 = displays["d4"])

os.close(fd)
