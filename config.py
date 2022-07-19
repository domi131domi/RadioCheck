import configparser as cp

_config_filename = 'config.ini'
_default_section = 'default'

data_path = None
sample_rate = 0
frames = 0
box_w_start = 0
box_w_end = 0
box_h_start = 0
box_h_end = 0
fs_cutoff = 0
min_fp_bar = 0
neighbourhood = 0
candidates_range = 1


def set_configuration(name=_default_section):
    config_parser = cp.ConfigParser()
    config_parser.read(_config_filename)
    config_section = config_parser[name]
    set_data(config_section)


def set_data(config_section):
    global data_path, sample_rate
    global box_w_start, box_w_end, box_h_start, box_h_end
    global frames, fs_cutoff, candidates_range
    global min_fp_bar, neighbourhood
    data_path = config_section['data_path']
    sample_rate = int(config_section['sample_rate'])
    box_w_start = int(config_section['box_w_start'])
    box_w_end = int(config_section['box_w_end'])
    box_h_start = int(config_section['box_h_start'])
    box_h_end = int(config_section['box_h_end'])
    frames = int(config_section['frames'])
    fs_cutoff = int(config_section['fs_cutoff'])
    min_fp_bar = int(config_section['min_fp_bar'])
    neighbourhood = int(config_section['neighbourhood'])
    candidates_range = int(config_section['candidates_range'])


def change_parameter(name, value):
    global data_path, sample_rate
    global box_w_start, box_w_end, box_h_start, box_h_end
    global frames, fs_cutoff
    global min_fp_bar
    try:
        match name:
            case "data_path":
                data_path = value
                return
            case "sample_rate":
                sample_rate = int(value)
                return
            case "box_w_start":
                box_w_start = int(value)
                return
            case "box_w_end":
                box_w_end = int(value)
                return
            case "box_h_start":
                box_h_start = int(value)
                return
            case "box_h_end":
                box_h_end = int(value)
                return
            case "frames":
                frames = int(value)
                return
            case "fs_cutoff":
                fs_cutoff = int(value)
                return
            case "min_fp_bar":
                min_fp_bar = int(value)
                return
            case "candidates_range":
                min_fp_bar = int(value)
                return
    except Exception as e:
        raise RuntimeError("Błąd ustawiania parametru")
    raise RuntimeError("Parametr nie istnieje")
