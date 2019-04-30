#!/usr/bin/env python2
from __future__ import print_function

import vxi11
import time
import argparse

from _rigol_channel import channels, save_channel_to_file
from _rigol_setting import disabled_beeper, locked_keyboard


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("DEVICE", nargs=1, help="Device to connect to")
    ap.add_argument("CHANNELS", nargs="*",
                    help="Channels to download, one of " + ", ".join(channels))
    args = ap.parse_args()
    device = args.DEVICE[0]
    selected_channels = args.CHANNELS if len(args.CHANNELS) > 0 else channels

    instrument = vxi11.Instrument(device)

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
