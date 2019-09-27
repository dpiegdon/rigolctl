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

    # set "printer" to screen-dump via GPIB
    dev.write("HCSU DEV,TIFFCOL,PORT,GPIB,PFEED,OFF,PENS,2,PSIZE,A4," +
              "CMDIV,1,AUTO,OFF,FORMAT,LANDSCAPE,BCKG,BLACK")

    # dump image
    image = b''
    chunksize = 16384
    try:
        dev.write("SCREEN_DUMP")
        while True:
            new_bit = dev.read(len=chunksize)
            image = image + new_bit
            if len(new_bit) != chunksize:
                break
    except gpib.GpibError:
        pass

    # set back to use internal printer for hardcopy
    dev.write("HCSU DEV,TIFFCOL,PORT,PRT,PFEED,OFF,PENS,2,PSIZE,A4," +
              "CMDIV,1,AUTO,OFF,FORMAT,LANDSCAPE,BCKG,BLACK")

    # put device back into local mode
    dev.ibloc()

    # store image to file
    filename = "screenshot_{}.tiff".format(time.time())
    with open(filename, 'wb+') as dumpfile:
        dumpfile.write(image)
        print(filename)
