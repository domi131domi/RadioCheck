from typing import Tuple

from audio import Audio
from fingerprint import FingerPrint


class DatabaseManager:

    def __init__(self):
        self.db = {}
        self.current_id = 0

    def save_fingerprints(self, fingerprints: list[FingerPrint]):
        for f in fingerprints:
            self.db[f.hash] = f.get_data()

    def get_best_fit(self, count: int, fingerprints: list[FingerPrint]):
        found_by_time = {}
        for fingerprint in fingerprints:
            if fingerprint.hash in self.db:
                time_audio: Tuple[int, Audio] = self.db[fingerprint.hash]
                key = (time_audio[0] - fingerprint.time, time_audio[1])
                if key in found_by_time:
                    found_by_time[key] += 1
                else:
                    found_by_time[key] = 1

        sorted_candidates = sorted(found_by_time.items(), key=lambda item: item[1], reverse=True)
        return sorted_candidates[:count]

    def clean(self):
        self.db = {}

    def get_new_id(self):
        self.current_id += 1
        return self.current_id

