#!python3
from sys import exit
from pathlib import Path
from shutil import copyfile
from socket import gethostname
from os import makedirs, path
import json


def export_configs(path_to_config_file, show_select_menu=False):
    settings = get_config_file(path_to_config_file)
    home = str(Path.home())
    dest = create_config_dir(settings['dest_dir'])
    file_to_colect = settings['colect_files']

    for conf in file_to_colect:
        if len(conf) > 2:
            opt_dir = create_optional_dir(dest, conf[2])
            copyfile(path.join( home, conf[0]), path.join(opt_dir, conf[1]))
        else:
            copyfile(path.join( home, conf[0]), path.join(dest, conf[1]))


def get_config_file(path_to_file):
    try:
        with open(path_to_file) as f:
            return json.load(f)
    except FileNotFoundError as e:
        print('Error: File does not exists')
        exit()


def create_optional_dir(dest, dir_name):
    """ Creates and Returns optional sub folder"""
    opt_folder = path.join(dest, dir_name)
    if not path.exists(opt_folder):
        makedirs(opt_folder)

    return opt_folder



def create_config_dir(dest_dir):
    """ Creates and  returns destination """
    home = str(Path.home())
    pc_name = gethostname()
    dest = path.join(home, dest_dir, pc_name )
    if not path.exists(dest):
        makedirs(dest)

    return dest;
