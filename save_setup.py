#!/usr/bin/env python2

import argparse
import pickle
import vxi11
from _rigol_setting import get_settings

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("DEVICE", nargs=1, help="Device to connect to")
    ap.add_argument("FILENAME", nargs=1, help="File to save setup to")
    args = ap.parse_args()
    device = args.DEVICE[0]
    filename = args.FILENAME[0]

    instrument = vxi11.Instrument(device)

    print(instrument.ask("*IDN?"))

    pickle.dump(get_settings(instrument), open(filename, 'wb'))
