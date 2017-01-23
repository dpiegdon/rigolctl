#!/usr/bin/env python2

import sys
import getopt
import vxi11

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("argument must be vxi11 identifier to device (e.g. hostname)")
        sys.exit(1)
    i = vxi11.Instrument(sys.argv[1])
    print(i.ask("*IDN?"))
    i.write(':STOP')
    for channel in ["CHAN1", "CHAN2", "CHAN3", "CHAN4", "MATH",
            "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", 
            "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15" ]:

        # select correct channel
        if channel.startswith("CHAN"):
            i.write(':WAV:MODE MAX')
            if int(i.ask(':{}:DISP?'.format(channel))) == 0:
                continue
        elif channel.startswith("MATH"):
            i.write(':WAV:MODE NORMAL')
            if int(i.ask(':{}:DISP?'.format(channel))) == 0:
                continue
        elif channel.startswith("D"):
            i.write(':WAV:MODE MAX')
            if int(i.ask(':LA:DISP? {}'.format(channel))) == 0:
                continue
        else:
            raise RuntimeError("invalid channel '{}'".format(channel))

        i.write(':WAV:SOUR {}'.format(channel))
        i.write(':WAV:FORM BYTE')

        preamble = i.ask(":WAV:PRE?").split(",")
        #print(preamble)
        memdepth = int(preamble[2])

        with open("capture_waveform_{}.raw".format(channel), "w") as dump:
            print("capture {} {} points".format(channel, memdepth))
            pos = 1
            while pos <= memdepth:
                chunksize = min(memdepth+1-pos, 500000)
                start = pos
                end = pos + chunksize - 1
                print("  {}..{}".format(start, end))
                i.write(':WAV:STAR {}'.format(start))
                i.write(':WAV:STOP {}'.format(end))
                chunk = i.ask_raw(':WAVEform:DATA?')
                pos += chunksize
                chunk = chunk[11:-1]
                dump.write(chunk)

