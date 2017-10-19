#!/bin/sh
if [ $# -lt 1 ]; then
	echo "$0 <wav data file> [further files...]"
	exit 1
fi
while [ $# -gt 0 ]; do
	WAV="$1"
	SR="$1.sr"
	echo "converting '$WAV' to '$SR'"
	sigrok-cli -i "$WAV" -o "$SR"
	shift
done;

