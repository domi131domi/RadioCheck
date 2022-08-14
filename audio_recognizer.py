import datetime
from typing import Tuple

import config
from audio import Audio


class AudioRecognizer:

    def __init__(self, mrc):
        self.max_result_count = mrc
        self.top_last_results = []
        self.current_summary = {}
        self.last_recognized = None

    def add_results(self, results):
        if len(self.top_last_results) == self.max_result_count:
            self.top_last_results.pop(0)

        self.top_last_results.append(results)
        self.generate_summary()

    def generate_summary(self):
        self.current_summary = {}
        for results in self.top_last_results:
            for result in results:
                key: Tuple[int, Audio] = result[0]
                count: int = result[1]
                if key in self.current_summary:
                    self.current_summary[key] += count
                else:
                    self.current_summary[key] = count

    def get_best_fit(self, current_time):
        sorted_summary = sorted(self.current_summary.items(), key=lambda item: item[1], reverse=True)
        if len(sorted_summary) > 0:
            best: Tuple[Tuple[int, Audio], int] = sorted_summary[0]
            print(str(best) + '  ' + str(datetime.timedelta(seconds=current_time)))
            if best[1] > config.min_fp_bar:  # mozliwe ze zmienic na % z maksymalnej liczby
                #print("Znaleziono moc:" + str(best[1]))
                best_name: Audio = best[0][1]
                if self.last_recognized != best_name:
                    self.last_recognized = best_name
                    return best_name.name, datetime.timedelta(seconds=current_time)
                    #print(str(best_name.name) + " " + str(best[1]) + " " + str(datetime.timedelta(seconds=current_time)))
        #self.last_recognized = None
        return None
