#!/usr/bin/env python2

from __future__ import print_function

import sys
import vxi11
import time

def dump_all_channels(instrument, record_id):
    for channel in ["CHAN1", "CHAN2", "CHAN3", "CHAN4", "MATH",
            "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", 
            "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15" ]:

        # skip channel if it is not displayed
        if channel.startswith("CHAN"):
            instrument.write(":waveform:mode max")
            if int(instrument.ask(":{}:display?".format(channel))) == 0:
                continue
        elif channel.startswith("MATH"):
            instrument.write(":waveform:mode normal")
            if int(instrument.ask(":{}:display?".format(channel))) == 0:
                continue
        elif channel.startswith("D"):
            instrument.write(":waveform:mode max")
            if int(instrument.ask(":LA:display? {}".format(channel))) == 0:
                continue
        else:
            raise RuntimeError("invalid channel '{}'".format(channel))

        # select channel
        instrument.write(":waveform:source {}".format(channel))
        instrument.write(":waveform:format byte")

        preamble = instrument.ask(":waveform:preamble?").split(",")

        memdepth = int(round(float(preamble[2])))
        ksps = int(round(1/float(preamble[4])/1000))
        yincE_6 = int(round(float(preamble[7])*1000*1000))

        print(" Channel {}, {} Points, {} KSa/s, YINC: {}E-6...  ".format(
                 channel, memdepth, ksps, yincE_6), end="")
        sys.stdout.flush()

        if(preamble[3] != "1"):
            print("  samples averaged over {} samples".format(preamble[3]))
            avg = "_{}avg".format(preamble[3])
        else:
            avg = ""

        filename = "{}_capture_waveform_{}{}_{}KSPS_yinc{}E-6{}.raw".format(
                                now,
                                ("" if -1 == record_id
                                    else ("REC%04d-" % record_id)),
                                channel,
                                ksps,
                                yincE_6,
                                avg)
        with open(filename, "w") as dump:
            pos = 1
            while pos <= memdepth:
                chunksize = min(memdepth+1-pos, 250000)
                start = pos
                end = pos + chunksize - 1
                print(" {}K-{}K".format(start/1000, end/1000), end="")
                sys.stdout.flush()
                instrument.write(":waveform:start {}".format(start))
                instrument.write(":waveform:stop {}".format(end))
                chunk = instrument.ask_raw(":waveform:data?")
                pos += chunksize
                chunk = chunk[11:-1]
                dump.write(chunk)
            print("")

    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("argument must be vxi11 identifier to device (e.g. hostname)")
        sys.exit(1)
    instrument = vxi11.Instrument(sys.argv[1])

    now = int(round(time.time()))

    print(instrument.ask("*idn?"))

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
        dump_all_channels(instrument, -1)
    else:
        for n in range(1, record_count+1):
            instrument.write(":function:wreplay:fcurrent {}".format(n))
            print("dumping record {} of {}".format(
                    instrument.ask(":function:wreplay:fcurrent?"),
                    record_count))
            dump_all_channels(instrument, n)

