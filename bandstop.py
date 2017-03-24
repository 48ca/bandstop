#!/usr/bin/env python3

import sys
if len(sys.argv) == 1:
    print("usage: ./bandstop.py <files>")
    sys.exit(1)

import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
from scipy.fftpack import fft

plt.ion()

N = 1000

def process(filename):
    fs, snd = wavfile.read(filename)

    samples, channels = snd.shape

    duration = samples/fs

    depth_type = snd.dtype

    if depth_type.num == 2:
        depth = 8
    elif depth_type.num == 3:
        depth = 16
    # elif depth_type == 4:
    #     depth = 24
    elif depth_type.num == 5:
        depth = 32
    else:
        print("Depth '{}' is unsupported".format(depth_type.name))
        exit(1)



    print("==== Information about {} ====".format(filename))
    print("Samples: {}".format(samples))
    print("Channels: {}".format(channels))
    print("Duration: {}".format(duration))
    print("Depth: {}-bit".format(depth))
    print("============================"+"="*len(filename))


    for c in range(channels):
        parse(snd.T[c], depth, samples, fs, duration)

def parse(sound_data, depth, samples, fs, duration):
    FFT_SAMPLE_SIZE = 10
    for i in range(0, samples, FFT_SAMPLE_SIZE*fs//1000):
        fft_data = fft(sound_data[i:(i+FFT_SAMPLE_SIZE*fs//1000)])
        real_length = len(fft_data)//2
        plt.plot(abs(fft_data[:(real_length-1)]),'r')
        plt.show()
        plt.pause(0.001)
        plt.clf()


for filename in sys.argv[1:]:
    process(filename)
