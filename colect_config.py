#!python3

from pathlib import Path
from shutil import copyfile
from socket import gethostname
from os import makedirs, path

home = str(Path.home())

settings = {
            'dest_dir':'Documents'
        }

# src dest optional_folder
config_files = [
            ['.config/i3/config', 'i3_config'],
            ['.config/i3status/config', 'i3status_config'],
            ['.Xresources', 'xresources'],
            ['.config/conky_widgets/conky_vim_shortcuts', 'conky_vim_shortcuts', 'conky_widgets'],
            ['.config/conky_widgets/shortcuts_maia', 'shortcuts_maia', 'conky_widgets'],
            ['.config/conky_widgets/conky_maia', 'conky_maia', 'conky_widgets'],
            ['Scripts/my_conky', 'my_conky', 'scripts']
        ]

def colect_configs():
    dest = create_config_dir(settings['dest_dir'])

    for conf in config_files:
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
