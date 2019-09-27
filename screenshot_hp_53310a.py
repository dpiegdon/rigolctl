#!/usr/bin/python

import sys
import Gpib
import gpib
import time

if __name__ == "__main__":
    if len(sys.argv) == 3:
        board_index, pad = int(sys.argv[1]), int(sys.argv[2])
    elif len(sys.argv) == 2:
        board_index, pad = 0, int(sys.argv[1])
    else:
        raise Exception("Parameters: [board_index] <pad>")

    dev = Gpib.Gpib(board_index, pad)

    dev.write("*IDN?")
    print(dev.read().decode().rstrip())

    # dump image
    try:
        image = b''
        chunksize = 16384
        dev.write("SYST:PRIN?")
        while True:
            new_bit = dev.read(len=chunksize)
            image = image + new_bit
            if len(new_bit) != chunksize:
                # FIXME: better test is to check SRQ, as mentioned in the
                # HP 53310a programming reference manual, Appendix D.
                break
    except gpib.GpibError:
        pass

    # store image to file
    t = time.time()
    filename = "screenshot_{}.pcl".format(t)
    with open(filename, 'wb+') as dumpfile:
        dumpfile.write(image)
        print(filename)

    print()
    print("you can convert PCL files with GhostPCL.")
    print("https://www.ghostscript.com/GhostPCL.html")
    print()
    print("gpcl6-927-linux-x86_64 -sDEVICE=pnggray -g640x480 -o " +
          "screenshot_{}.png {}".format(t, filename))
