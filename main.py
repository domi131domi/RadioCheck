from main_controller import MainController
import time_printer as tp

m = MainController()
command = None


while command != "x":
    command = input(">")
    spl = command.split(" ")
    m.read_command(spl[0], spl[1])
