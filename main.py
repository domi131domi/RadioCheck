from main_controller import MainController
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--learn', action="store", dest='learn', default=None, nargs='*')
parser.add_argument('--find', action="store", dest='find', default=None, nargs='*')
parser.add_argument('--data_path', action="store", dest='data_path', default=None, nargs=1)
parser.add_argument('--result_path', action="store", dest='result_path', default=None, nargs=1)
parser.add_argument('--clean', action="store_true", dest='clean')
args = parser.parse_args()

if args.learn is not None or args.find is not None:
    if args.learn is None or args.find is None:
        raise RuntimeError("Flaga --learn i --find muszą być ustawione w trybie flagowym")
    m = MainController()
    m.init_args(args)
    m.run_flag_mode()
    exit()

m = MainController()
command = None

print("Wpisz help aby uzyskac pomoc\n")


while command != "x":
    try:
        command = input(">")
        spl = command.split(" ")
        m.read_command(spl)
    except Exception as e:
        print("Error: " + str(e))
