#!/usr/bin/env python2

import sys
import pickle
import vxi11
from _rigol_setting import get_settings

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("{} <device> <filename>".format(sys.argv[0]))
        print(" - <device>:   vxi11 identifier to device (e.g. hostname)")
        print(" - <filename>: where to save the setup")
        sys.exit(1)
    instrument = vxi11.Instrument(sys.argv[1])

    print(instrument.ask("*IDN?"))

    pickle.dump(get_settings(instrument), open(sys.argv[2], 'wb'))
