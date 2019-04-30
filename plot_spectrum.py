#!/usr/bin/python2
from __future__ import print_function

import argparse
import numpy as np
import matplotlib.pyplot as plt
import re


def plot_spec(data, sample_rate, filename):
    values = np.array(bytearray(data))
    nfft = 2**12
    plt.specgram(values, nfft, sample_rate, noverlap=2**8)
    plt.ylim(50e6, 80e6)
    plt.grid(True)
    plt.show(block=True)
    if filename is not None:
        plt.savefig(filename)
        print("saved as '{}'".format(filename))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('INFILE', nargs=1, help='Channeldump file to plot')
    ap.add_argument('OUTFILE', nargs='?', help='Filename for plot (as PNG)')
    args = ap.parse_args()
    infile = args.INFILE[0]
    outfile = args.OUTFILE

    with open(infile, "r") as inf:
        data = inf.read()

    regex = re.compile(r'^([A-Za-z0-9]*)_capture_waveform_([A-Z0-9]*)' +
                       '_ksps(\d*)_yinc([^_]*)_yref([^_]*).u8$')
    match = regex.match(infile)
    ksps = int(match.group(3))

    plot_spec(data, ksps*1000, outfile)
