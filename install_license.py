#!/usr/bin/env python2

import sys
import vxi11
import termios
import time

def Dp800_set(instrument, key):
    return( instrument.write(":LIC:SET " + key) )

def Dp800_get(instrument):
    return instrument.ask("*OPT?")

def Dp800_restart(instrument):
    return instrument.write("*RST")

def MsoDs1000Z_set(instrument, key):
    return( instrument.write(":system:option:install " + key) )

def MsoDs1000Z_get(instrument):
    return( "[reading options not supported for MSO/DS1000z devices]")

devicefunctions = {
        'DP831A':   { 'set': Dp800_set,      'get': Dp800_get      },
        'DP831':    { 'set': Dp800_set,      'get': Dp800_get      },
        'DP832A':   { 'set': Dp800_set,      'get': Dp800_get      },
        'DP832':    { 'set': Dp800_set,      'get': Dp800_get      },
        'DP821A':   { 'set': Dp800_set,      'get': Dp800_get      },
        'DP821':    { 'set': Dp800_set,      'get': Dp800_get      },
        'DP811A':   { 'set': Dp800_set,      'get': Dp800_get      },
        'DP811':    { 'set': Dp800_set,      'get': Dp800_get      },
        'DS1054Z':  { 'set': MsoDs1000Z_set, 'get': MsoDs1000Z_get },
        'DS1074Z':  { 'set': MsoDs1000Z_set, 'get': MsoDs1000Z_get },
        'DS1104Z':  { 'set': MsoDs1000Z_set, 'get': MsoDs1000Z_get },
        'MSO1074Z': { 'set': MsoDs1000Z_set, 'get': MsoDs1000Z_get },
        'MSO1104Z': { 'set': MsoDs1000Z_set, 'get': MsoDs1000Z_get },
}

if __name__ == "__main__":
    pname = sys.argv[0]
    sys.argv = sys.argv[1:]

    invert = "off"
    color = "on"

    instrument = vxi11.Instrument(sys.argv[0])
    
    idn = instrument.ask("*IDN?")
    print(idn)
    idn = idn.split(",")
    device = idn[1].upper()
    serial = idn[2].upper()

    print("device: " + device)
    print("serial: " + serial)

    if device not in devicefunctions:
        print("setting options for device '" + device + "'currently not supported.")

    while True:
        print("installed options: " + devicefunctions[device]["get"](instrument))
        time.sleep(0.1)
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
        key = raw_input("key> ")
        if(key == ""):
            break
        print("trying to install: " + key)
        print(devicefunctions[device]["set"](instrument, key))

