#!/usr/bin/env python2

import vxi11
import argparse


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("DEVICE", nargs=1, help="Device to connect to")
    args = ap.parse_args()
    device = args.DEVICE[0]

    instrument = vxi11.Instrument(device)

    print(instrument.ask("*IDN?"))

    while(True):
        err = instrument.ask(":system:error?")
        print(err)
        if(err == '0,"No error"'):
            break
