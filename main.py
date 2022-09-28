#!/usr/bin/python3

# imports
import random as rnd
import wave
import time
import sys
import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound
from scipy.io.wavfile import write

if len(sys.argv) == 1:
    print("Must specify encoding level. Like between 10 and 70. But it is somewhat random so try different values. Like: 10,20,30,35,32.")
    exit(1)
level = int(sys.argv[1])

rnd.seed(time.time() + 123451)


def Transform(path: str):
    raw = wave.open(path)
    signal = raw.readframes(-1)
    np_signal = np.frombuffer(signal, dtype="int16")
    f_rate = raw.getframerate()

    new_signal = [np.add(np_signal[x], (rnd.random() * 100)) for x in range(len(np_signal))]
    randomlist = []
    for i in range(0, 99):
        n = rnd.randint(level // 8, level)
        randomlist.append(n)
    new_signal = np.convolve(new_signal, n)  # [10, 4, 16, 4, 10, 30, 30, 2, 5, 5, 5, 5]

    new_signal = [np.add(new_signal[x], (rnd.random() * 100)) for x in range(len(new_signal))]
    # new_signal = gaussian_filter(new_signal, sigma=1)

    return new_signal, f_rate


def UnTransform(path: str):
    raw = wave.open(path)
    signal = raw.readframes(-1)
    np_signal = np.frombuffer(signal, dtype="int16")
    f_rate = raw.getframerate()
    np_signal = [np.add(np_signal[x], 10000) for x in range(len(np_signal))]

    new_signal = np_signal

    return new_signal, f_rate


def SaveSound(signal, f_rate, filename="output.wav"):
    scaled = np.int16(signal)
    write(filename, f_rate, scaled)
    return filename


def PlaySound(filename):
    playsound(filename)


def visualize(signal, f_rate):
    time = np.linspace(
        0,
        len(signal) / f_rate,
        num=len(signal)
    )
    plt.figure(1)
    plt.title("Sound Wave")
    plt.xlabel("Time")
    plt.plot(time, signal)
    plt.show()


def Disguise():
    signal, f_rate = Transform("test.wav")  # change test.wav to the file you want to process.
    fn = SaveSound(signal, f_rate, "output.wav")  # Save output file as output.wav
    #visualize(signal, f_rate)


if __name__ == "__main__":
    Disguise()
    i = input("Do you want to play the output y/N: ")
    if i == "yes" or i == "y":
        PlaySound("output.wav")
