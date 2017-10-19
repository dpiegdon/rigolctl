#!/bin/sh
if [ $# -lt 1 ]; then
	echo "$0 <raw data file> [further files...]"
	exit 1
fi
while [ $# -gt 0 ]; do
	RAW="$1"
	WAV="$1.wav"
	echo "converting '$RAW' to '$WAV'"
	sox -t raw -b 8 -e unsigned-integer -r 44100 -c 1 $RAW $WAV
	shift
done;

