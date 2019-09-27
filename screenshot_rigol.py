#!/usr/bin/env python2

import vxi11
import time
import argparse

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("DEVICE", nargs=1, help="Device to connect to")
    ap.add_argument("--invert", "-i", action="store_true",
                    help="Invert color in plot")
    ap.add_argument("--nocolor", "-n", action="store_true",
                    help="Plot in monochrome")
    args = ap.parse_args()
    device = args.DEVICE[0]
    invert = "on" if args.invert else "off"
    color = "off" if args.nocolor else "on"

    instrument = vxi11.Instrument(device)

    print(instrument.ask("*IDN?"))

    now = int(round(time.time()))
    filename = "{}_capture_screen.png".format(now)

    with open(filename, "w") as dump:
        img = instrument.ask_raw(':disp:data? '+color+','+invert+',png')
        img = img[11:]
        dump.write(img)

    print("plot saved as: {}".format(filename))
