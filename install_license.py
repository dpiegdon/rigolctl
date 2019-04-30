#!/usr/bin/env python2

from __future__ import print_function
import vxi11
import argparse


def Dp800_set(instrument, key):
    return instrument.write(":LIC:SET " + key)


def Dp800_get(instrument):
    return instrument.ask("*OPT?")


def Dp800_restart(instrument):
    return instrument.write("*RST")


def MsoDs1000Z_set(instrument, key):
    return instrument.write(":system:option:install " + key)


def MsoDs1000Z_get(instrument):
    return "[reading options not supported for MSO/DS1000z devices]"


devicefunctions = {
         'DP831A':   {'set': Dp800_set, 'get': Dp800_get},
         'DP831':    {'set': Dp800_set, 'get': Dp800_get},
         'DP832A':   {'set': Dp800_set, 'get': Dp800_get},
         'DP832':    {'set': Dp800_set, 'get': Dp800_get},
         'DP821A':   {'set': Dp800_set, 'get': Dp800_get},
         'DP821':    {'set': Dp800_set, 'get': Dp800_get},
         'DP811A':   {'set': Dp800_set, 'get': Dp800_get},
         'DP811':    {'set': Dp800_set, 'get': Dp800_get},
         'DS1054Z':  {'set': MsoDs1000Z_set, 'get': MsoDs1000Z_get},
         'DS1074Z':  {'set': MsoDs1000Z_set, 'get': MsoDs1000Z_get},
         'DS1104Z':  {'set': MsoDs1000Z_set, 'get': MsoDs1000Z_get},
         'MSO1074Z': {'set': MsoDs1000Z_set, 'get': MsoDs1000Z_get},
         'MSO1104Z': {'set': MsoDs1000Z_set, 'get': MsoDs1000Z_get},
}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("DEVICE", nargs=1, help="Device to connect to")
    args = ap.parse_args()
    device = args.DEVICE[0]

    instrument = vxi11.Instrument(device)

    idn = instrument.ask("*IDN?")
    print(idn)
    idn = idn.split(",")
    device = idn[1].upper()
    serial = idn[2].upper()

    print("device: " + device)
    print("serial: " + serial)

    if device not in devicefunctions:
        print("setting options for device '" +
              device + "'currently not supported.")

    while True:
        print("installed options: " +
              devicefunctions[device]["get"](instrument))
        key = raw_input("key> ")
        if(key == ""):
            break
        print("trying to install: " + key)
        print(devicefunctions[device]["set"](instrument, key))
