import os
import soundfile as sf
import config
from audio import Audio
import librosa


class AudioReader:

    def __init__(self, audio: Audio):
        self.path = config.data_path
        self.sound_file = None
        self.file_samplerate = None
        self.filename = audio.name
        self.converted_file = None

        self.convert_to_wav()
        self.dtime = 0

    def convert_to_wav(self):
        return self.convert_to_wav_soundfile()

    def read_block(self):
        return self.read_block_soundfile()

    def close(self):
        return self.close_soundfile()

    def convert_to_wav_soundfile(self):
        try:
            filename = self.path + self.filename
            name, ext = os.path.splitext(filename)
            ext_name = '.wav'
            if ext != ext_name:
                print("Converting to " + ext_name + ": " + filename)
                os.system('ffmpeg -y -i "%s" "%s%s" 2> logsFfmpeg.txt' % (filename, name, ext_name))
                print("Converted")
                filename = name + ext_name
                self.converted_file = filename
            self.sound_file = sf.SoundFile(filename)
            self.file_samplerate = self.sound_file.samplerate
        except Exception as e:
            raise RuntimeError("Błąd konwertowania pliku", e)

    def read_block_soundfile(self):
        sig = self.sound_file.read(dtype='float32', frames=config.frames)
        dtime = self.dtime
        self.dtime += (config.frames / self.sound_file.samplerate)
        return sig, dtime

    def close_soundfile(self):
        self.sound_file.close()
        os.remove(self.filename)

