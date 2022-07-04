from audio_recognizer import AudioRecognizer
from database_manager import DatabaseManager
import config
from audio_reader import AudioReader
from audio_editor import AudioEditor
from fingerprint import FingerPrint
import time
import datetime
import time_printer as tp
import debug_peak_saver as dps


class MainController:

    def __init__(self):
        print("Run")
        self.db = DatabaseManager()
        config.set_configuration()
        self.last_recognized = None
        self.last_delta = None
        self.time_counter = 0

    def read_command(self, command, value):
        if command == "learn":
            self.learn_audio(value)
        elif command == "find":
            self.find_in_audio(value)
        elif command == "test":
            self.run_test(value)
        elif command == "save":
            tp.save_times_with_percentage(value, "Main find in audio")
        elif command == "path":
            config.data_path = value

    def learn_audio(self, name):
        ar = AudioReader(name)
        file_data, signal, dtime = ar.read_block()
        while len(signal > 0):
            ae = AudioEditor(signal, file_data)
            spectrogram = ae.prepare_data()
            fp = FingerPrint(spectrogram, name)
            res = fp.get_fingerprints()
            self.db.save_fingerprints(res)
            file_data, signal, dtime = ar.read_block()

        print("Learnt " + name)
        dps.song = 2

    def find_in_audio(self, name):
        ar = AudioReader(name)
        tp.start("Main find in audio")
        tp.start("AudioReader")
        file_data, signal, dtime = ar.read_block()
        tp.stop("AudioReader")
        fit = None
        recognizer = AudioRecognizer(5)
        while len(signal > 0):
            tp.start("AudioEditor")
            ae = AudioEditor(signal, file_data)
            spectrogram = ae.prepare_data()
            tp.stop("AudioEditor")
            tp.start("FingerPrint")
            fp = FingerPrint(spectrogram, name)
            fingerprinted2 = fp.get_fingerprints()
            tp.stop("FingerPrint")

            tp.start("Db best fit")
            res = self.db.get_best_fit(10, fingerprinted2)
            tp.stop("Db best fit")
            tp.start("Recognizer")
            recognizer.add_results(res)
            recognizer.print_highest_value(dtime)
            tp.stop("Recognizer")

            tp.start("AudioReader")
            file_data, signal, dtime = ar.read_block()
            tp.stop("AudioReader")

        tp.stop("Main find in audio")
        dps.load()

    def run_test(self, value):
        if value == '1':
            self.read_command("learn", "reklama_mikolajkowy1.mp3")
            self.read_command("learn", "reklama_mikolajkowy2.mp3")
            self.read_command("learn", "reklama_mikolajkowy3.mp3")
            self.read_command("find", "mikolajkowy.mp3")
        if value == '2':
            self.read_command("learn", "reklama_mikolajkowy1.mp3")
            self.read_command("learn", "reklama_mikolajkowy2.mp3")
            self.read_command("learn", "reklama_mikolajkowy3.mp3")
            self.read_command("find", "blok_mikolajkowy.mp3")
        if value == '3':
            self.read_command("learn", "reklama_mikolajkowy1.wav")
            self.read_command("learn", "reklama_mikolajkowy2.wav")
            self.read_command("learn", "reklama_mikolajkowy3.wav")
            self.read_command("learn", "test3_reklama1.wav")
            self.read_command("find", "test3_blok.wav")