import string

_DEFAULT_ID = -1


def get_audio_for_only_name(name: string):
    return Audio(name, _DEFAULT_ID)


class Audio:

    def __init__(self, name: string, ID: int):
        self.name = name
        self.ID = ID
        self.datetime_start = None
        self.datetime_stop = None
