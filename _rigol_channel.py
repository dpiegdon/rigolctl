#
from __future__ import print_function

import sys

channels = ["CHAN1", "CHAN2", "CHAN3", "CHAN4", "MATH",
        "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7",
        "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15"]


def get_channel(instrument, channel):
    """ download specified channel.
    returns a tuple of
        (
            ksps,           -- sample frequency in Kilo Samples Per Seconds
            yincE_6         -- y-axis increment * 10^6
            yref            -- y reference level
            avg             -- number of samples each point was averaged from
            memdepth        -- memory depth (length) of channel
            data            -- actual data, as raw string
        )

    """
    # skip channel if it is not displayed
    if channel.startswith("CHAN"):
        instrument.write(":waveform:mode max")
        if int(instrument.ask(":{}:display?".format(channel))) == 0:
            print("Channel {}: skipped, not displayed".format(channel))
            return None
    elif channel.startswith("MATH"):
        instrument.write(":waveform:mode normal")
        if int(instrument.ask(":{}:display?".format(channel))) == 0:
            print("Channel {}: skipped, not displayed".format(channel))
            return None
    elif channel.startswith("D"):
        instrument.write(":waveform:mode max")
        if int(instrument.ask(":LA:display? {}".format(channel))) == 0:
            print("Channel {}: skipped, not displayed".format(channel))
            return None
    else:
        raise RuntimeError("invalid channel '{}'".format(channel))

    # select channel
    instrument.write(":waveform:source {}".format(channel))
    instrument.write(":waveform:format byte")

    preamble = instrument.ask(":waveform:preamble?").split(",")

    memdepth = int(round(float(preamble[2])))
    ksps = int(round(1 / float(preamble[4]) / 1000))
    yincE_6 = int(round(float(preamble[7]) * 1000 * 1000))
    yref = int(round(float(preamble[9])))
    avg = int(preamble[3])

    print("Channel {}, {} Points, KSPS {}, YINC {}E-6, YREF {}, AVG {}...". \
            format(channel, memdepth, ksps, yincE_6, yref, avg), end="")
    sys.stdout.flush()

    data = r''
    pos = 1
    while pos <= memdepth:
        chunksize = min(memdepth + 1 - pos, 250000)
        start = pos
        end = pos + chunksize - 1
        print(" {}K-{}K".format(start / 1000, end / 1000), end="")
        sys.stdout.flush()
        instrument.write(":waveform:start {}".format(start))
        instrument.write(":waveform:stop {}".format(end))
        chunk = instrument.ask_raw(":waveform:data?")
        pos += chunksize
        chunk = chunk[11:-1]
        data += chunk

    print("\nCollecting data done.")
    return (ksps, yincE_6, yref, avg, memdepth, data)


def save_channel_to_file(instrument, prefix, channel, record_id=None):
    """ save channel to file
    filename is automatically generated, see below.

    prefix      -- prefix to use in filename
    channel     -- channel to download
    record_id   -- None or an integer (counter) specifying which record was set.
    """
    value = get_channel(instrument, channel)
    if value is None:
        return False
    (ksps, yincE_6, yref, avg, _, data) = value

    filename = "{}_capture_waveform_{}{}_ksps{}_yinc{}E-6_yref{}{}.u8".format(
            prefix,
            ("" if record_id is None
                    else ("REC%04d_" % record_id)),
            channel,
            ksps,
            yincE_6,
            yref,
            "" if avg == 1 else "_avg{}".format(avg)
            )
    with open(filename, "w") as dump:
        dump.write(data)
    return True
