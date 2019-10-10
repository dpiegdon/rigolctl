#!/usr/bin/env python2

import vxi11
import time
import argparse



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("DEVICE", nargs=1, help="Device to connect to")
    ap.add_argument("--toggle", "-t",
                    action="store_const", dest="action", const="toggle",
                    default=None, help="Toggle channel")
    ap.add_argument("--wait", "-w", type=float, help="Seconds to wait after changes", default=1)
    ap.add_argument("--on", action="store_const", dest="action", const="on")
    ap.add_argument("--off", action="store_const", dest="action", const="off")
    ap.add_argument("--channel", "-c", type=int, help="Select channel", default=1)
    ap.add_argument("--volt", "-v", type=float, help="Set voltage", default=None)
    ap.add_argument("--amp", "-a", type=float, help="Set current", default=None)
    args = ap.parse_args()

    instrument = vxi11.Instrument(args.DEVICE[0])
    print(instrument.ask("*IDN?"))

    print("CHANNEL  {}".format(args.channel))

    if args.action is not None:
        if args.action == "toggle":
            current_state = instrument.ask(":OUTPUT:STATE? CH{}".format(args.channel)).upper()
            new_state = "ON" if current_state == "OFF" else "OFF"
        elif args.action == "on":
            new_state = "ON"
        elif args.action == "off":
            new_state = "OFF"

        instrument.write(":OUTPUT:STATE CH{},{}".format(args.channel, new_state))
        time.sleep(args.wait)

    print("output   " + instrument.ask(":OUTPUT:STATE? CH{}".format(args.channel)).upper())

    if args.volt is not None:
        instrument.write(":SOURCE{}:VOLTAGE {}".format(args.channel, args.volt))
    print("set volt " + instrument.ask(":SOURCE{}:VOLTAGE?".format(args.channel)))

    if args.amp is not None:
        instrument.write(":SOURCE{}:CURRENT {}".format(args.channel, args.amp))
    print("set amp  " + instrument.ask(":SOURCE{}:CURRENT?".format(args.channel)))

    measured = instrument.ask(":MEASURE:ALL? CH{}".format(args.channel)).split(",")
    print("measured volt {}".format(measured[0]))
    print("measured amp  {}".format(measured[1]))
    print("measured watt {}".format(measured[2]))
