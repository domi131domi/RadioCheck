import sys

import numpy as np
import scipy.io.wavfile
import scipy.signal
from matplotlib import mlab, pyplot as plt
from scipy.signal import spectrogram
from scipy import ndimage
import time_printer as tp

import config


class AudioEditor:

    def __init__(self, signal, file_sample_rate):
        self.signal = signal
        self.sample_rate = config.sample_rate
        self.file_sample_rate = file_sample_rate
        self.fs = None
        self.times = None
        self.amplitudes = None

    def prepare_data(self):
        tp.start("AudioEditor: change_to_mono")
        self.signal = change_to_mono(self.signal)
        tp.stop("AudioEditor: change_to_mono")
        tp.start("AudioEditor: change_sample_rate")
        self.signal = change_sample_rate(self.signal, self.file_sample_rate, self.sample_rate)
        tp.stop("AudioEditor: change_sample_rate")
        tp.start("AudioEditor: spectrogram")
        self.amplitudes, self.fs, self.times = mlab.specgram(
            self.signal,
            Fs=self.sample_rate,
            NFFT=config.nfft,
            window=mlab.window_hanning,
            noverlap=int(config.nfft * 0.5))
        tp.stop("AudioEditor: spectrogram")
        tp.start("AudioEditor: log")
        logAmplitudes = 10 * np.log10(self.amplitudes, out=np.zeros_like(self.amplitudes), where=(self.amplitudes != 0))
        logAmplitudes[logAmplitudes == 0] = -sys.maxsize
        tp.stop("AudioEditor: log")
        return logAmplitudes[:config.fs_cutoff, :]


def change_to_mono(sig):
    if len(sig.shape) > 1:
        return np.mean(sig, axis=1)
    return sig


def change_sample_rate(data, rate_from, rate_to):
    if rate_from == rate_to:
        return data
    return scipy.signal.resample(data, int(len(data) / rate_from * rate_to))


def get_index_range(f, min_f, max_f):
    start = 0
    end = 0
    for idx, x in enumerate(f):
        if x <= min_f:
            start = idx + 1
            continue
        if x >= max_f:
            end = idx - 1
            break
    return start, end


def filter_frequencies(f, amplitudes, min_f, max_f):
    start, end = get_index_range(f, min_f, max_f)
    return f[start:end], amplitudes[start:end]


def find_local_max(data):
    neighborhood = np.ones((3, 3), dtype=bool)
    max_filter = ndimage.maximum_filter(data, footprint=neighborhood)
    a = np.array(data)
    b = np.array(max_filter)
    local_max = (a == b)
    return local_max
