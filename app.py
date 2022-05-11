import os, sys
from fcntl import ioctl
from .scripts.ioctl_cmds import *
from .scripts.board import DE2i

if len(sys.argv) < 2:
    print("Error: expected more command line arguments")
    print("Syntax: %s </dev/device_file>"%sys.argv[0])
    exit(1)

fd = os.open(sys.argv[1], os.O_RDWR)

board = DE2i(fd)

board.set_display("right", d1 = 1, d2 = 1, d3 = 1, d4 = 1)

os.close(fd)
