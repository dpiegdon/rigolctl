#!/usr/bin/python2
from __future__ import print_function

import argparse
import numpy as np
import matplotlib.pyplot as plt
import re

ap = argparse.ArgumentParser()
ap.add_argument('FILE', nargs=1, help='File to load')
args = ap.parse_args()

filename=args.FILE[0]

with open(filename, "r") as load:
    data = load.read()

def plot_spec(data, sample_rate):
    values = np.array(bytearray(data))
    nfft= 2**12
    plt.specgram(values, nfft, sample_rate, noverlap=2**8)
    plt.ylim(50e6,80e6)
    plt.grid(True)
    plt.show(block=True)

regex = re.compile(r'^([A-Za-z0-9]*)_capture_waveform_([A-Z0-9]*)_ksps(\d*)_yinc([^_]*)_yref([^_]*).u8$')
match = regex.match(filename)
ksps = int(match.group(3))

plot_spec(data, ksps*1000)
