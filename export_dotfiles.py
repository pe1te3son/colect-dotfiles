#!python3

from pathlib import Path
from shutil import copyfile
from socket import gethostname
from os import makedirs, path
import json
home = str(Path.home())

settings = None

with open(path.join(path.dirname(path.realpath(__file__)), 'settings.json'), 'r') as f:
    settings = json.load(f)

def colect_configs():
    dest = create_config_dir(settings['dest_dir'])
    file_to_colect = settings['colect_files']
    for conf in file_to_colect:
        if len(conf) > 2:
            opt_dir = create_optional_dir(dest, conf[2])
            copyfile(path.join( home, conf[0]), path.join(opt_dir, conf[1]))
        else:
            copyfile(path.join( home, conf[0]), path.join(dest, conf[1]))
        

def create_optional_dir(dest, dir_name):
    """ Creates and Returns optional sub folder"""
    opt_folder = path.join(dest, dir_name)
    if not path.exists(opt_folder):
        makedirs(opt_folder)

    return opt_folder



def create_config_dir(dest_dir):
    """ Creates and  returns destination """
    pc_name = gethostname()
    dest = path.join(home, dest_dir, pc_name )
    if not path.exists(dest):
        makedirs(dest)

    return dest;


colect_configs()
