#!/usr/bin/env python2

import vxi11
import pickle
import argparse

from _rigol_setting import set_settings


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("DEVICE", nargs=1, help="Device to connect to")
    ap.add_argument("FILENAME", nargs=1, help="File to load setup from")
    args = ap.parse_args()
    device = args.DEVICE[0]
    filename = args.FILENAME[0]

    instrument = vxi11.Instrument(device)

    print(instrument.ask("*IDN?"))

    saved_settings = pickle.load(open(filename, 'r'))
    set_settings(instrument, saved_settings)
