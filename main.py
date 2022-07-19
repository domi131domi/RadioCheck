from main_controller import MainController
import time_printer as tp

m = MainController()
command = None

print("Wpisz help aby uzyskac pomoc\n")
while command != "x":
    #try:
        command = input(">")
        spl = command.split(" ")
        m.read_command(spl)
    #except Exception as e:
    #    print("Error: " + str(e))
