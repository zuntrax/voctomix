#!/bin/sh
ffmpeg -y \
	-i $HOME/avsync.ts \
	-vf scale=1920x1080 \
	-c:v rawvideo \
	-c:a pcm_s16le \
	-f matroska \
	tcp://localhost:10000
