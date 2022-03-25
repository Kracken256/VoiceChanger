# imports
import datetime
import random as rnd
import wave
import time

import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound
from scipy.io.wavfile import write

rnd.seed(time.time() + 123451)


def Transform(path: str):
    raw = wave.open(path)
    signal = raw.readframes(-1)
    np_signal = np.frombuffer(signal, dtype="int16")
    f_rate = raw.getframerate()

    new_signal = [np.add(np_signal[x], (rnd.random() * 100)) for x in range(len(np_signal))]
    randomlist = []
    for i in range(0, 999):
        n = rnd.randint(1, 5)
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
    signal, f_rate = Transform("Recording.wav")  # change test.wav to the file you want to process.
    fn = SaveSound(signal, f_rate, "output.mp3")  # Save output file as output.mp3
    visualize(signal, f_rate)


if __name__ == "__main__":
    Disguise()
