#!/usr/bin/env python2

import sys
import vxi11
import time

if __name__ == "__main__":
    pname = sys.argv[0]
    sys.argv = sys.argv[1:]

    def abort_with_help():
        print("{} [invert] <device>".format(pname))
        print(" - invert:     invert plot colors")
        print(" - nocolor:    plot without color")
        print(" - <device>:   vxi11 identifier to device (e.g. hostname)")
        sys.exit(1)

    invert = "off"
    color = "on"

    if len(sys.argv) == 0:
        abort_with_help()

    while len(sys.argv) > 1:
        if sys.argv[0] == "invert":
            invert = "on"
        elif sys.argv[0] == "nocolor":
            color = "off"
        else:
            print("unknown statement '{}'".format(sys.argv[0]))
            abort_with_help()
        sys.argv = sys.argv[1:]

    instrument = vxi11.Instrument(sys.argv[0])

    print(instrument.ask("*IDN?"))

    now = int(round(time.time()))
    filename = "{}_capture_screen.png".format(now)

    with open(filename, "w") as dump:
        img = instrument.ask_raw(':disp:data? '+color+','+invert+',png')
        img = img[11:]
        dump.write(img)

    print("plot saved as: {}".format(filename))
