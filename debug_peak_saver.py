
song = 1

peaks1 = []
peaks2 = []


def save_peaks(peak):
    if song == 1:
        peaks1.append(peak)
    elif song == 2:
        peaks2.append(peak)


def load():
    a = 0

