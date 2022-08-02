from audio import Audio, get_audio_for_only_name
from audio_recognizer import AudioRecognizer
from database_manager import DatabaseManager
import config
from audio_reader import AudioReader
from audio_editor import AudioEditor
from fingerprint import FingerPrinter
import time_printer as tp
import csv

class MainController:

    def __init__(self):
        print("Run")
        self.db = DatabaseManager()
        config.set_configuration()
        self.last_recognized = None
        self.last_delta = None
        self.time_counter = 0
        self.recognized_audio = []

    def read_command(self, command):
        if command[0] == "help":
            print(HELP_TEXT)
            return
        elif command[0] == "clean":
            self.db.clean()
            return
        if len(command) < 2:
            raise RuntimeError("Niepoprawna komenda lub jej wykorzystanie; Komenda: " + str(command))
        if command[0] == "learn":
            self.learn_audio(command[1])
            return
        elif command[0] == "find":
            self.find_in_audio(command[1])
            return
        elif command[0] == "save_times":
            tp.save_times_with_percentage(command[1], "Main find in audio")
            return
        elif command[0] == "save":
            self.save_to_csv(command[1])
            return
        elif command[0] == "from_file":
            self.read_from_file(command[1])
            return
        if len(command) < 3:
            raise RuntimeError("Niepoprawna komenda lub jej wykorzystanie; Komenda: " + str(command))
        if command[0] == "change":
            config.change_parameter(command[1], command[2])
            return
        else:
            raise RuntimeError("Niepoprawna komenda lub jej wykorzystanie; Komenda: " + str(command))

    def learn_audio(self, name):
        audio = Audio(name, self.db.get_new_id())
        audio_reader = AudioReader(audio)
        file_data = audio_reader.sound_file

        signal, dtime = audio_reader.read_block()
        while len(signal > 0):
            audio_editor = AudioEditor(signal, file_data)
            signal = audio_editor.prepare_data()
            finger_printer = FingerPrinter(signal, audio)
            res = finger_printer.get_fingerprints()
            self.db.save_fingerprints(res)
            signal, dtime = audio_reader.read_block()

        print("Learnt " + name)

    def find_in_audio(self, name):
        audio = get_audio_for_only_name(name)
        audio_reader = AudioReader(audio)
        file_data = audio_reader.sound_file

        signal, dtime = audio_reader.read_block()
        recognizer = AudioRecognizer(5)
        while len(signal > 0):
            audio_editor = AudioEditor(signal, file_data)
            spectrogram = audio_editor.prepare_data()
            fingerprinter = FingerPrinter(spectrogram, audio)
            fingerprints = fingerprinter.get_fingerprints()
            res = self.db.get_best_fit(10, fingerprints)
            recognizer.add_results(res)
            best = recognizer.get_best_fit(dtime)
            if best is not None:
                self.recognized_audio.append(best)
            # if name is not None:
            # print(" z " + str(self.db.get_max_fp(name)))
            signal, dtime = audio_reader.read_block()

    def read_from_file(self, filename):
        file = open(filename, 'r')
        lines = file.readlines()
        for line in lines:
            spl = [x.strip() for x in line.split(' ')]
            self.read_command(spl)

    def save_to_csv(self, filename):
        with open(filename + '.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["Nazwa", "Czas wystąpienia"])
            for row in self.recognized_audio:
                writer.writerow(row)


HELP_TEXT = "Dostępne komendy: \n\nlearn [nazwa_pliku.roz] - dodaj plik do rozpoznawania\nfind [nazwa_pliku.roz] - wyszukaj pliki dodane przez komende learn w podanym pliku\nfrom_file [nazwa.txt] - wczytanie komend z pliku\nchange [parametr] [wartość] - zmień wartość parametru\nclean - resetuje nauczone nagrania\n"
