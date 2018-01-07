#!python3
from sys import exit
from shutil import copyfile
from socket import gethostname
from os import makedirs, path, remove, rmdir
from lib import utils
from pathlib import Path


def export_configs(path_to_config_file, show_select_menu=False):
    settings = utils.get_config_file(path_to_config_file)
    dest = get_config_dir(settings['dest_dir'])
    file_to_colect = settings['colect_files']

    for conf in file_to_colect:
        export_single(conf, dest)


def export_single(conf, destination_dir):
    conf[0] = utils.parse_home_path(conf[0])

    if len(conf) > 2:
        opt_dir = create_optional_dir(destination_dir, conf[2])
        copyfile( conf[0], path.join(opt_dir, conf[1]))
    else:
        copyfile( conf[0], path.join(destination_dir, conf[1]))


def find_dotfile_duplicate(new_dotfile, arr):
    for idx, dotfile in enumerate(arr):
        if dotfile[0] == new_dotfile[0]:
            return idx

    return -1


def replace_dotfile_config(new_dotfile, dotfile_array):
    dotfile_array[find_dotfile_duplicate(new_dotfile, dotfile_array)] = new_dotfile


def remove_empty_dir(path_to_dir):
    try:
        rmdir(path_to_dir)
    except OSError:
        return


def remove_old_dotfile_copy(dotfile, dest):
    path_to_remove_file = None
    if len(dotfile) > 2:
        path_to_remove_file = path.join(get_config_dir(dest), dotfile[2], dotfile[1])
    else: 
        path_to_remove_file = path.join(get_config_dir(dest), dotfile[1])

    if path.exists(path_to_remove_file):
        remove(path_to_remove_file)
        # Remove empty dir
        if len(dotfile) > 2:
            remove_empty_dir(path.join(get_config_dir(dest), dotfile[2]))


def add_new_dotfile_to_config(new_dotfile, config_file):
    has_duplicate = find_dotfile_duplicate(new_dotfile, config_file['colect_files']) 

    if has_duplicate > -1:
        overwrite = input("["+ new_dotfile[0] +"] already maintained. overwrite? y/n: ")
        if overwrite.lower() == 'y':
            remove_old_dotfile_copy(config_file['colect_files'][has_duplicate], config_file['dest_dir'])
            replace_dotfile_config(new_dotfile, config_file['colect_files']) 
    else:
        config_file['colect_files'].append(new_dotfile)

    return config_file


def add_new_config(new_dotfile, path_to_config_file, show_select_menu=False):
    settings = utils.get_config_file(path_to_config_file)
    dest = get_config_dir(settings['dest_dir'])

    settings = add_new_dotfile_to_config(new_dotfile, settings)

    utils.overwrite_config_file(path_to_config_file, settings)
    export_single(new_dotfile, dest)


def create_optional_dir(dest, dir_name):
    """ Creates and Returns optional sub folder"""
    opt_folder = path.join(dest, dir_name)
    if not path.exists(opt_folder):
        makedirs(opt_folder)

    return opt_folder


def get_config_dir(dest_dir):
    """ Creates and  returns destination """
    dest_dir = utils.parse_home_path(dest_dir) 

    pc_name = gethostname()
    dest = path.join( dest_dir, pc_name )
    if not path.exists(dest):
        makedirs(dest)

    return dest;
