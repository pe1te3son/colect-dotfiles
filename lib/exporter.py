#!python3
from sys import exit
from shutil import copyfile
from socket import gethostname
from os import makedirs, path
from lib import utils

def export_configs(path_to_config_file, show_select_menu=False):
    settings = utils.get_config_file(path_to_config_file)
    home = utils.get_home()
    dest = create_config_dir(settings['dest_dir'])
    file_to_colect = settings['colect_files']

    for conf in file_to_colect:
        export_single(conf, dest, home)


def export_single(conf, destination_dir, home):
        if len(conf) > 2:
            opt_dir = create_optional_dir(destination_dir, conf[2])
            copyfile(path.join( home, conf[0]), path.join(opt_dir, conf[1]))
        else:
            copyfile(path.join( home, conf[0]), path.join(destination_dir, conf[1]))


def add_new_config(new_config_file_path, path_to_config_file, show_select_menu=False):
    # TODO: finish this up
    settings = utils.get_config_file(path_to_config_file)
    home = utils.get_home()
    dest = create_config_dir(settings['dest_dir'])
    print(new_config_file_path) 
    print(path_to_config_file) 


def create_optional_dir(dest, dir_name):
    """ Creates and Returns optional sub folder"""
    opt_folder = path.join(dest, dir_name)
    if not path.exists(opt_folder):
        makedirs(opt_folder)

    return opt_folder



def create_config_dir(dest_dir):
    """ Creates and  returns destination """
    home = utils.get_home()
    pc_name = gethostname()
    dest = path.join(home, dest_dir, pc_name )
    if not path.exists(dest):
        makedirs(dest)

    return dest;
