import hashlib
import string

import numpy as np
from scipy.ndimage import maximum_filter
import config
from audio import Audio


class Point:

    def __init__(self, x, y):
        self.time = x
        self.frequency = y


class FingerPrint:

    def __init__(self, _hash: string, time: int, audio: Audio):
        self.hash = _hash
        self.time = time
        self.audio = audio

    def get_data(self):
        return self.time, self.audio


class FingerPrinter:

    def __init__(self, signal, audio: Audio):
        self.local_max_idx = None
        self.signal = signal
        self.audio = audio

    def get_fingerprints(self):
        self.local_max_idx = find_local_max(self.signal)
        fingerprints = []
        for idx in range(0, len(self.local_max_idx)):
            freq, time = self.local_max_idx[idx]
            candidates = get_candidates(idx, self.local_max_idx)
            for candidate_freq, candidate_time in candidates:
                fingerprints.append(create_fingerprint(
                    Point(time, freq),
                    Point(candidate_time, candidate_freq),
                    self.audio))

        return fingerprints


def find_local_max(signal):
    max_filter = maximum_filter(signal, size=config.neighbourhood, mode='constant', cval=0.0)
    local_max = (signal == max_filter)
    idx_freq, idx_times = np.where(local_max)
    pairs = list(zip(idx_freq, idx_times))
    pairs.sort(key=lambda pair: pair[1])  # sortowanie po czasie
    return pairs


def get_candidates(idx, local_maxes):
    anchor_freq, anchor_time = local_maxes[idx]
    box_w_start = anchor_time + config.box_w_start
    box_w_end = anchor_time + config.box_w_end
    box_h_start = anchor_freq + config.box_h_start
    box_h_end = anchor_freq + config.box_h_end
    max_range = len(local_maxes)
    for i in range(1, config.candidates_range):
        if (idx + i) >= max_range:
            break
        if box_h_end >= local_maxes[idx + i][0] > box_h_start and box_w_end >= local_maxes[idx + i][1] > box_w_start:
            yield local_maxes[idx + i]


def create_fingerprint(p1: Point, p2: Point, audio: Audio):
    return FingerPrint(create_sha(p1.frequency, p2.frequency, p2.time - p1.time), p1.time, audio)


def create_sha(freq1, freq2, delta_time):
    return hashlib.sha256((str(freq1) + str(freq2) + str(delta_time)).encode('utf8')).hexdigest()
