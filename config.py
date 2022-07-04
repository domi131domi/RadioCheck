import configparser as cp

# names
import config

_config_filename = 'config.ini'
_default_section = 'default'

data_path = None

# audio editor
min_f = 0
max_f = 0
sample_rate = 0
frames = 0

#fingerprint
nperseg = 0
maxes_percentage = 0
box_w_start = 0
box_w_end = 0
box_h_start = 0
box_h_end = 0
percentage_of_fp = 0
fs_cutoff = 0
max_fs_bar = 0


def set_configuration(name=_default_section):
    config_parser = cp.ConfigParser()
    config_parser.read(_config_filename)
    config_section = config_parser[name]
    set_data(config_section)


def set_data(config_section):
    global data_path, min_f, max_f, sample_rate, nperseg, maxes_percentage
    global box_w_start, box_w_end, box_h_start, box_h_end
    global frames, percentage_of_fp, fs_cutoff, max_fs_bar
    data_path = config_section['data_path']
    min_f = int(config_section['min_f'])
    max_f = int(config_section['max_f'])
    sample_rate = int(config_section['sample_rate'])
    nperseg = int(config_section['nperseg'])
    maxes_percentage = float(config_section['maxes_percentage'])
    box_w_start = int(config_section['box_w_start'])
    box_w_end = int(config_section['box_w_end'])
    box_h_start = int(config_section['box_h_start'])
    box_h_end = int(config_section['box_h_end'])
    frames = int(config_section['frames'])
    percentage_of_fp = float(config_section['percentage_of_fp'])
    fs_cutoff = int(config_section['fs_cutoff'])
    max_fs_bar = float(config_section['max_fs_bar'])

