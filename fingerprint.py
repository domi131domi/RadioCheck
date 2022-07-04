import hashlib
from scipy import ndimage
import numpy as np
import config
import debug_peak_saver as dps


class Point:

    def __init__(self, x, y):
        self.time = x
        self.frequency = y


class FingerPrint:

    def __init__(self, amplitudes, song_name):
        self.local_max_idx = None
        self.amplitudes = amplitudes
        self.song_name = song_name

    def create_local_max(self):
        self.local_max_idx = find_local_max(self.amplitudes)

    def get_fingerprints(self):
        self.create_local_max()
        fingerprints = []
        for idx in range(0, len(self.local_max_idx)):
            y, x = self.local_max_idx[idx]
            candidates = get_candidates(idx, self.local_max_idx)
            for candidate_y, candidate_x in candidates:
                fingerprints.append(create_fingerprint(
                    Point(x, y),
                    Point(candidate_x, candidate_y),
                    self.song_name))

        return fingerprints


def find_local_max(data):
    neighborhood = np.ones((3, 3), dtype=bool)
    max_filter = ndimage.maximum_filter(data, footprint=neighborhood)
    bar = data.max() * config.max_fs_bar
    mask = np.where(data <= bar)
    local_max = (data == max_filter)
    local_max[mask] = False
    dps.save_peaks(local_max)
    fs, times = np.where(local_max)
    res = list(zip(fs, times))
    res.sort(key=lambda x: -data[x])
    #count = int(len(res) * config.maxes_percentage)
    res = [x for x in res]#[:count]
    res.sort(key=lambda x: x[1])
    return res


def get_candidates(idx, local_maxes):
    y, x = local_maxes[idx]
    box_w_start = x + config.box_w_start
    box_w_end = x + config.box_w_end
    box_h_start = y + config.box_h_start
    box_h_end = y + config.box_h_end
    r = 10
    for i in range(1, 100):
        if (idx + i) < len(local_maxes):
            if box_h_end >= local_maxes[idx + i][0] > box_h_start and box_w_end >= local_maxes[idx + i][1] > box_w_start:
                yield local_maxes[idx+i]


def filter_and_zip_local_max(y_max, x_max, data):
    values_max = data[y_max, x_max]
    sorted_args = values_max.argsort()[::-1]
    #count = int(sorted_args.shape[0] * config.maxes_percentage)
    #return [(y_max[idx], x_max[idx]) for idx in sorted_args][:count]
    return [(y_max[idx], x_max[idx]) for idx in sorted_args]


def create_fingerprint(p1: Point, p2: Point, song_name):
    return create_sha(p1.frequency, p2.frequency, p2.time - p1.time), p1.time, song_name


def create_sha(f1, f2, delta_time):
    return hashlib.sha256((str(f1) + str(f2) + str(delta_time)).encode('utf8')).hexdigest()
