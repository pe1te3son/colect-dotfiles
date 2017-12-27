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

def import_configs():
    config_dir = settings['dest_dir']
    file_to_import = settings['colect_files']
    for conf in file_to_import:
        current_config_dir = path.join(home, config_dir, gethostname())
        
        copy_file = input('Overwrite: ' + path.join(conf[0]) + ' (y/n) ')

        if copy_file == 'y':
            if len(conf) > 2:
                opt_dir = path.join(current_config_dir, conf[2])
                copyfile(path.join(opt_dir, conf[1]), path.join( home, conf[0]))
            else:
                copyfile(path.join(current_config_dir, conf[1]), path.join( home, conf[0]))
            
            print ('Copied...')
        else:
            print ('Skipped...')

import_configs()
