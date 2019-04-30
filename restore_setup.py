#!/usr/bin/env python2

import sys
import vxi11
import pickle
from _rigol_setting import set_settings

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("{} <device> <filename>".format(sys.argv[0]))
        print(" - <device>:   vxi11 identifier to device (e.g. hostname)")
        print(" - <filename>: where to save the setup")
        sys.exit(1)
    instrument = vxi11.Instrument(sys.argv[1])

    print(instrument.ask("*IDN?"))

    saved_settings = pickle.load(open(sys.argv[2], 'r'))
    set_settings(instrument, saved_settings)
