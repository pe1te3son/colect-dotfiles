#!python3

from sys import argv, exit
from pathlib import Path
from shutil import copyfile
from socket import gethostname
from os import makedirs, path
import json

args = argv[1:]


def import_configs():
    home = str(Path.home())
    settings = get_config_file(args[0])
    config_dir = settings['dest_dir']
    file_to_import = settings['colect_files']
    for conf in file_to_import:
        current_config_dir = path.join(home, config_dir, gethostname())

        copy_file = input('Overwrite: ' + path.join(conf[0]) + ' [ Default (n)o ]\n(y)es (n)o (e)xit : ')

        if copy_file == 'y':
            if len(conf) > 2:
                opt_dir = path.join(current_config_dir, conf[2])
                copyfile(path.join(opt_dir, conf[1]), path.join( home, conf[0]))
            else:
                copyfile(path.join(current_config_dir, conf[1]), path.join( home, conf[0]))

            print ('Copied...')
        elif copy_file == 'e':
            exit()
        else:
            print ('Skipped...')



def get_config_file(path_to_file):
    try:
        with open(path_to_file) as f:
            return json.load(f)
    except FileNotFoundError as e:
        print('Error: File does not exists')
        exit()



if not len(args):
    print('Requires path to config file as an argument')
else:
    import_configs()
