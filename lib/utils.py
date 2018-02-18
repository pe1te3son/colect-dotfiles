from pathlib import Path
import json
from os import path


def get_home():
    return str(Path.home())


def get_config_file(path_to_file):
    try:
        with open(path_to_file) as f:
            return json.load(f)
    except FileNotFoundError as e:
        print('Error: File does not exists')
        exit()


def overwrite_config_file(path_to_file, json_to_write):
    try:
        with open(path_to_file, "w", encoding="utf-8") as f:
            json.dump(json_to_write, f, ensure_ascii=False)
    except FileNotFoundError as e:
        print('Error: File does not exists')
        exit()


def parse_home_path(file_path):
    if file_path.startswith('~'):
        file_path = path.join(get_home(), file_path[2:])

    return file_path
