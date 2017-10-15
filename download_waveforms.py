#!/usr/bin/env python2
from __future__ import print_function

import sys
import vxi11
import time

from _rigol_channel import channels, save_channel_to_file
from _rigol_setting import disabled_beeper, locked_keyboard

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("{} <device> [channel [channel [...]]]".format(sys.argv[0]))
        print(" - <device>:   vxi11 identifier to device (e.g. hostname)")
        print(" - [channel]:  channel to dump. one of: " + ", ".join(channels))
        sys.exit(1)
    instrument = vxi11.Instrument(sys.argv[1])

    if len(sys.argv) > 2:
        selected_channels = sys.argv[2:];
        for c in selected_channels:
            if c not in channels:
                print("unknown channel '{}'. aborting.".format(c))
                sys.exit(1)
    else:
        selected_channels = channels

    print("Download channels: " + ", ".join(selected_channels))
    print(instrument.ask("*idn?"))

    with disabled_beeper(instrument), locked_keyboard(instrument):
        now = int(round(time.time()))
        record_count = -1
        # only stop if not in waveform recording mode and not actually
        # recording right now. it would restart recording in that case.
        if 1 != int(instrument.ask(":function:wrecord:enable?")):
            instrument.write(":stop")
        elif "STOP" != instrument.ask(":function:wrecord:operate?"):
            instrument.write(":function:wrecord:operate stop")

        if(1 == int(instrument.ask(":function:wrecord:enable?"))):
            instrument.write(":function:wreplay:stop")
            instrument.write(":function:wreplay:fstart 1")
            record_count = int(instrument.ask(":function:wreplay:fmax?"))
            instrument.write(":function:wreplay:fend {}".format(record_count))

        if record_count < 0:
            for ch in selected_channels:
                save_channel_to_file(instrument, now, ch, None)
        else:
            for n in range(1, record_count+1):
                instrument.write(":function:wreplay:fcurrent {}".format(n))
                print("dumping record {} of {}".format(
                        instrument.ask(":function:wreplay:fcurrent?"),
                        record_count))
                for ch in selected_channels:
                    save_channel_to_file(instrument, now, ch, n)

