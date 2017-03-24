#!/usr/bin/env python3

import sys
if len(sys.argv) == 1:
    print("usage: ./bandstop.py <files>")
    sys.exit(1)

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.fftpack import fft, fftfreq

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


    # for c in range(channels):
    #    parse(snd.T[c], depth, samples, fs, duration)
    parse(snd.T[0], depth, samples, fs, duration)

def find_outstanding_frequencies(data, points_per_sample, fs):
    # THRESHOLD = 5000000
    diff_data = np.diff(data)
    low_band = points_per_sample//4 # Half of our divided version
    high_ind = np.argpartition(diff_data[low_band:], -5)[-5:] + low_band
    low_ind = np.argpartition(diff_data[low_band:], 5)[:5] + low_band
    # np.where(data[high_ind] > THRESHOLD * points_per_sample, high_ind, 0)
    sys.stdout.write("h indices: ")
    print(fs/points_per_sample * (high_ind))
    sys.stdout.write("l indeces: ")
    print(fs/points_per_sample * (low_ind))
    # print(fs/points_per_sample * data[high_ind])
    for x in high_ind:
        plt.axvline(x=x, color='b')
    for x in low_ind:
        plt.axvline(x=x, color='g')

def parse(sound_data, depth, samples, fs, duration):
    FFT_SAMPLE_SIZE = 1000 # 100 milliseconds
    points_per_sample = FFT_SAMPLE_SIZE*fs//1000
    frequency_data = fftfreq(points_per_sample, FFT_SAMPLE_SIZE/1000)*points_per_sample * FFT_SAMPLE_SIZE/1000
    frequency_conversion_ratio = fs/points_per_sample
    for i in range(0, samples, points_per_sample):
        fft_data = fft(sound_data[i:(i+points_per_sample)])
        real_length = len(fft_data)//2
        real_data = abs(fft_data[:(real_length-1)])

        plt.plot(real_data,'r')
        plt.show()
        plt.pause(0.2)
        plt.clf()

        find_outstanding_frequencies(real_data, points_per_sample, fs)


for filename in sys.argv[1:]:
    process(filename)
