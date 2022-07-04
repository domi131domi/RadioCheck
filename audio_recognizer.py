import datetime


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
                key = result[0]
                count = result[1]
                if key in self.current_summary:
                    self.current_summary[key] += count
                else:
                    self.current_summary[key] = count

    def print_highest_value(self, current_time):
        sorted_summary = sorted(self.current_summary.items(), key=lambda item: item[1], reverse=True)
        if len(sorted_summary) > 0:
            best = sorted_summary[0]
            if best[1] > 100:
                best_name = best[0][1]
                if self.last_recognized != best_name:
                    print("\n\n")
                    self.last_recognized = best_name
                    print(str(best_name) + " " + str(datetime.timedelta(seconds=current_time)))
