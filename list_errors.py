#!/usr/bin/env python2

import sys
import vxi11
import time

if __name__ == "__main__":
    pname = sys.argv[0]
    sys.argv = sys.argv[1:]

    def abort_with_help():
        print("{} <device>".format(pname))
        print(" - <device>:   vxi11 identifier to device (e.g. hostname)")
        sys.exit(1)

    if len(sys.argv) != 1:
        abort_with_help()

    instrument = vxi11.Instrument(sys.argv[0])
    
    print(instrument.ask("*IDN?"))

    while(True):
        err = instrument.ask(":system:error?")
        print(err)
        if(err == '0,"No error"'):
            break;

