#!/usr/bin/env python2

import sys
import vxi11
import time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("argument must be vxi11 identifier to device (e.g. hostname)")
        sys.exit(1)
    i = vxi11.Instrument(sys.argv[1])

    print(i.ask("*IDN?"))

    now = int(round(time.time()))

    with open("{}_capture_screen.png".format(now), "w") as dump:
        img = i.ask_raw(':DISP:DATA? on,off,png')
        img = img[11:]
        dump.write(img)

