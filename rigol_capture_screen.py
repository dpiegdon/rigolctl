#!/usr/bin/env python2

import sys
import getopt
import vxi11

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("argument must be vxi11 identifier to device (e.g. hostname)")
        sys.exit(1)
    i = vxi11.Instrument(sys.argv[1])
    print(i.ask("*IDN?"))
    with open("capture_screen.png", "w") as dump:
        img = i.ask_raw(':DISP:DATA? on,off,png')
        img = img[11:]
        dump.write(img)

