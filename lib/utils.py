from pathlib import Path
import json


def get_home():
    return str(Path.home())


def get_config_file(path_to_file):
    try:
        with open(path_to_file) as f:
            return json.load(f)
    except FileNotFoundError as e:
        print('Error: File does not exists')
        exit()

