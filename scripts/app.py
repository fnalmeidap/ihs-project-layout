from app-ioctl-example import DE2i

import os, sys
from fcntl import ioctl
from ioctl_cmds import *

if __name__ == "__main__":

    if len(sys.argv) < 2:
    print("Error: expected more command line arguments")
    print("Syntax: %s </dev/device_file>"%sys.argv[0])
    exit(1)

    fd = os.open(sys.argv[1], os.O_RDWR)
    board = DE2i(fd)