#!/usr/bin/env python2

import sys
import vxi11
import time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("argument must be vxi11 identifier to device (e.g. hostname)")
        sys.exit(1)
    i = vxi11.Instrument(sys.argv[1])

    now = int(round(time.time()))

    print(i.ask("*IDN?"))

    # FIXME: only STOP when not stopped yet. pressing STOP in record mode will start new recording.
    i.write(':STOP')

    for channel in ["CHAN1", "CHAN2", "CHAN3", "CHAN4", "MATH",
            "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", 
            "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15" ]:

        # skip channel if it is not displayed
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

        # select channel
        i.write(':WAV:SOUR {}'.format(channel))
        i.write(':WAV:FORM BYTE')

        preamble = i.ask(":WAV:PRE?").split(",")
        print(preamble)

        memdepth = int(round(float(preamble[2])))
        print("  {} Points".format(memdepth))

        ksps = int(round(1/float(preamble[4])/1000))
        print("  {} KSa/s".format(ksps))

        yincE_6 = int(round(float(preamble[7])*1000*1000))
        print("  YINC: {}E-6".format(yincE_6))

        if(preamble[3] != "1"):
            print("  samples averaged over {} samples".format(preamble[3]))
            avg = "_{}avg".format(preamble[3])
        else:
            avg = ""

        with open("{}_capture_waveform_{}_{}KSPS_yinc{}E-6{}.raw".format(now, channel, ksps, yincE_6, avg), "w") as dump:
            pos = 1
            while pos <= memdepth:
                chunksize = min(memdepth+1-pos, 250000)
                start = pos
                end = pos + chunksize - 1
                print("    {}..{}".format(start, end))
                i.write(':WAV:STAR {}'.format(start))
                i.write(':WAV:STOP {}'.format(end))
                chunk = i.ask_raw(':WAVEform:DATA?')
                pos += chunksize
                chunk = chunk[11:-1]
                dump.write(chunk)

