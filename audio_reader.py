import os
import soundfile as sf
import numpy as np

import config


class AudioReader:

    def __init__(self, filename):
        self.path = config.data_path
        self.sound_file = None
        self.filename = filename
        self.convert_to_wav()
        self.dtime = 0

    def convert_to_wav(self):
        filename = self.path + self.filename
        name, ext = os.path.splitext(filename)
        if ext != 'wav':
            os.system('ffmpeg -y -i "%s" "%s%s" 2> logsFfmpeg.txt' % (filename, name, '.wav'))
            filename = name + '.wav'
        self.sound_file = sf.SoundFile(filename)

    def read_block(self):
        sig = self.sound_file.read(dtype='float64', frames=config.frames)
        dtime = self.dtime
        self.dtime += config.frames/self.sound_file.samplerate
        return self.sound_file, sig, dtime

    def close(self):
        self.sound_file.close()
        os.remove(self.filename)
