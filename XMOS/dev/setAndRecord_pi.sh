python3 ~/Desktop/I2S_Device/TLV/ref/old/i2s_4ch_slave.py &&\
	arecord -D plughw:3,0 -c 2 -r 48000 -f S32_LE -t wav -V stereo -v file.wav
