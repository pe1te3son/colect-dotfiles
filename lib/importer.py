#!python3

from sys import exit
from pathlib import Path
from shutil import copyfile
from socket import gethostname
from os import makedirs, path
import json


def import_configs(path_to_config_file, show_select_menu=False):
    settings = get_config_file(path_to_config_file)
    config_dir = settings['dest_dir']
    files_to_import = settings['colect_files']
    home_folder = get_home()
    current_config_dir = path.join(home_folder, config_dir, gethostname())

    if show_select_menu:
        menu_selection = print_select_menu(files_to_import)

        if menu_selection == "c":
            exit()
        elif type(menu_selection) is list:
            for idx in menu_selection:
                import_single(files_to_import[idx], current_config_dir, home_folder)
            return

    for conf in files_to_import:
        import_single(conf, current_config_dir, home_folder)


def print_select_menu(files_to_import):
    print("Select files to import; example: 1,2,3\n")
    for idx, val in enumerate(files_to_import):
        print(str(idx + 1) + ". " + val[0])
    
    print("\n\t(a)ll\t(c)ancel\n")
    
    user_selection = None
    while not valid_user_selection(user_selection, files_to_import):
        user_selection = input("select: ")

    return parse_user_selection(user_selection)


def parse_user_selection(user_selection):
    if user_selection == "a" or user_selection == "c":
        return user_selection

    return [ int(x) - 1 for x in user_selection.split(",") ]


def valid_user_selection(user_selection, files_to_import):
    if not user_selection:
        return False

    if user_selection == "a" or user_selection == "c":
        return True

    selected_values = user_selection.split(",")
    for val in selected_values:
        if val.isnumeric() and int(val) - 1 < len(files_to_import):
            continue
        else:
            print("Invalid option(s)")
            return False

    return True


def get_home():
    return str(Path.home())


def import_single(conf, current_config_dir, home):
    print(conf[0] + " ..... ok")
    if len(conf) > 2:
        opt_dir = path.join(current_config_dir, conf[2])
        copyfile(path.join(opt_dir, conf[1]), path.join( home, conf[0]))
    else:
        copyfile(path.join(current_config_dir, conf[1]), path.join( home, conf[0]))


def get_config_file(path_to_file):
    try:
        with open(path_to_file) as f:
            return json.load(f)
    except FileNotFoundError as e:
        print('Error: File does not exists')
        exit()

