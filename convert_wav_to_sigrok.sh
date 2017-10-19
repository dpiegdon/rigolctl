#!/bin/sh
if [ $# -ne 1 ] || [ ! -e $1 ]; then
	echo "$0 <wav data file>"
	exit 1
fi
WAV="$1"
SR="$1.sr"
sigrok-cli -i "$WAV" -o "$SR"
