
class DatabaseManager:

    def __init__(self):
        self.db = {}

    def save_fingerprints(self, fingerprints):
        for f in fingerprints:
            value = (f[1], f[2])
            if f[0] in self.db:
                if value not in self.db[f[0]]:
                    #self.db[f[0]].append(value)
                    self.db[f[0]] = [value]
            else:
                self.db[f[0]] = [value]

    def get_best_fit(self, count, fingerprints):
        found_by_time = {}
        for fingerprint in fingerprints:
            if fingerprint[0] in self.db:
                audio_list = self.db[fingerprint[0]]
                for name_and_time in audio_list:
                    key = (name_and_time[0] - fingerprint[1], name_and_time[1])
                    if key in found_by_time:
                        found_by_time[key] += 1
                    else:
                        found_by_time[key] = 1

        sorted_candidates = sorted(found_by_time.items(), key=lambda item: item[1], reverse=True)
        return sorted_candidates[:count]
