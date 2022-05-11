import os, sys
from fcntl import ioctl
from scripts.board import DE2i

fd = os.open("/dev/mydev", os.O_RDWR)

board = DE2i(fd)

board.set_display("right", d1 = 1, d2 = 1, d3 = 1, d4 = 1)

os.close(fd)
