#!/bin/sh
if [ $# -ne 1 ] || [ ! -e $1 ]; then
	echo "$0 <raw data file>"
	exit 1
fi
RAW="$1"
WAV="$1.wav"
sox -t raw -b 8 -e unsigned-integer -r 44100 -c 1 $RAW $WAV
