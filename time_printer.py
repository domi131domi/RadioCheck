import datetime
import time

measurements = {}


def start(category: str):
    if category in measurements:
        if measurements[category].start is None:
            measurements[category].start = time.time()
            measurements[category].stop = None
    else:
        measurements[category] = TimeMeasure(category)
        measurements[category].start = time.time()


def stop(category: str):
    if category in measurements:
        if measurements[category].stop is None:
            measurements[category].stop = time.time()
            measurements[category].delta += measurements[category].stop - measurements[category].start
            measurements[category].start = None


def save_times(filename):
    python_file = open(filename, "w")
    for category in measurements:
        python_file.write(str(category) + ' : ' + time_to_str(measurements[category].delta) + '\n')
    python_file.close()


def save_times_with_percentage(filename, main_category):
    python_file = open(filename, "w")
    for category in measurements:
        prc = int(measurements[category].delta / measurements[main_category].delta * 100)
        python_file.write(str(category) + ' : ' + time_to_str(measurements[category].delta) + ' ' + str(prc) + '%' + '\n')
    python_file.close()


def time_to_str(seconds):
    return str(datetime.timedelta(seconds=seconds))


class TimeMeasure:

    def __init__(self, category):
        self.start = None
        self.stop = None
        self.delta = 0
        self.category = category
