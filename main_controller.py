import datetime
import re
import os
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

    def init_args(self, args):
        self.args = args
        if self.args.data_path is not None:
            config.data_path = self.args.data_path[0]

    def __init__(self):
        print("Run")
        self.db = DatabaseManager()
        config.set_configuration()
        self.last_recognized = None
        self.last_delta = None
        self.time_counter = 0
        self.recognized_audio = []
        self.last_audio: Audio = None
        self.args = None
        self.files_to_clean = []

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
        if audio_reader.converted_file is not None:
            self.files_to_clean.append(audio_reader.converted_file)
        file_samplerate = audio_reader.file_samplerate

        signal, dtime = audio_reader.read_block()
        while len(signal > 0):
            audio_editor = AudioEditor(signal, file_samplerate)
            signal = audio_editor.prepare_data()
            finger_printer = FingerPrinter(signal, audio)
            res = finger_printer.get_fingerprints()
            self.db.save_fingerprints(res)
            signal, dtime = audio_reader.read_block()

        print("Learnt " + name)

    def find_in_audio(self, name):
        tp.start("Main find")
        print("Finding in " + name)
        self.recognized_audio = []
        self.last_audio = audio = get_audio_for_only_name(name)
        startdate, enddate = get_dates_from_name(name)
        audio.datetime_start = startdate
        audio.datetime_stop = enddate

        audio_reader = AudioReader(audio)
        if audio_reader.converted_file is not None:
            self.files_to_clean.append(audio_reader.converted_file)
        file_samplerate = audio_reader.file_samplerate

        signal, dtime = audio_reader.read_block()
        recognizer = AudioRecognizer(1)
        while len(signal > 0):
            audio_editor = AudioEditor(signal, file_samplerate)
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

        tp.stop("Main find")

    def read_from_file(self, filename):
        file = open(filename, 'r')
        lines = file.readlines()
        for line in lines:
            spl = [x.strip() for x in line.split(' ')]
            self.read_command(spl)

    def save_to_csv(self, filename, result_path=None):
        if self.last_audio is None:
            return
        if result_path is not None:
            path = result_path
        else:
            path = config.data_path
        with open(path + filename + '.csv', 'w') as file:
            file.write("Nazwa pliku przeszukiwanego;" + self.last_audio.name + "\n")
            has_declared_dates = self.last_audio.datetime_start is not None and self.last_audio.datetime_stop is not None
            if has_declared_dates:
                file.write("Czas UTC rozpoczecia;" + str(self.last_audio.datetime_start) + "\n")
                file.write("Czas UTC zakonczenia;" + str(self.last_audio.datetime_stop) + "\n")
            file.write("Czas analizy;" + str(datetime.timedelta(seconds=tp.measurements["Main find"].delta)) + "\n")
            writer = csv.writer(file, delimiter=';')

            if has_declared_dates:
                writer.writerow(["Nazwa", "Czas wystąpienia w pliku", "Czas wystąpienia UTC"])
                for row in self.recognized_audio:
                    date = str(self.last_audio.datetime_start + row[1])
                    writer.writerow(row + (date, ))
            else:
                writer.writerow(["Nazwa", "Czas wystąpienia w pliku"])
                for row in self.recognized_audio:
                    writer.writerow(row)

    def run_flag_mode(self):
        all_learn_files = get_learn_files(self.args.learn)
        all_find_files = get_learn_files(self.args.find)
        for learn_file in all_learn_files:
            self.learn_audio(learn_file)

        for find_file in all_find_files:
            self.find_in_audio(find_file)
            self.save_to_csv('find_' + str(find_file).replace('/', '_').split('.')[0], self.args.result_path[0])

        if self.args.clean:
            for file in self.files_to_clean:
                if os.path.isfile(file):
                    os.remove(file)


def get_learn_files(files):
    all_files = []
    learn_files = files
    for learn_file in learn_files:
        if str(learn_file).endswith('/'):
            files = [f for f in os.listdir(config.data_path + learn_file) if os.path.isfile(os.path.join(config.data_path + learn_file, f))]
            for file in files:
                all_files.append(learn_file + file)
        else:
            all_files.append(learn_file)
    return make_files_distinct(all_files)


def make_files_distinct(files):
    names = {}
    for file in files:
        name = str(file).split('.')[0]
        ext = str(file).split('.')[1]
        if name in names:
            if ext == 'wav':
                names[name] = file
        else:
            names[name] = file
    return names.values()

HELP_TEXT = "Dostępne komendy: \n\nlearn [nazwa_pliku.roz] - dodaj plik do rozpoznawania\nfind [nazwa_pliku.roz] - wyszukaj pliki dodane przez komende learn w podanym pliku\nfrom_file [nazwa.txt] - wczytanie komend z pliku\nchange [parametr] [wartość] - zmień wartość parametru\nclean - resetuje nauczone nagrania\n"

date_regex = r'(\d{4})_(\d{2})_(\d{2})_(\d{2})_(\d{2})_(\d{2})_(\d{4})_(\d{2})_(\d{2})_(\d{2})_(\d{2})_(\d{2})'


def get_dates_from_name(name):
    match = re.search(date_regex, name)
    if match:
        groups = match.groups()
        startdate = datetime.datetime(int(groups[0]), int(groups[1]), int(groups[2]), int(groups[3]), int(groups[4]), int(groups[5]))
        enddate = datetime.datetime(int(groups[6]), int(groups[7]), int(groups[8]), int(groups[9]), int(groups[10]), int(groups[11]))
        return startdate, enddate

    return None, None
