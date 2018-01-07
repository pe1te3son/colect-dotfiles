#!/bin/python3
from sys import argv, exit
import getopt 
from getpass import getuser
from lib import exporter, importer
import os

def is_import(args):
    return "--import" in args or "-i" in args


def is_export(args):
    return "--export" in args or "-e" in args


def is_select_menu(args):
    return "--select-menu" in args or "-s" in args


def is_add_config(args):
    return "--add" in args or "-a" in args


def has_config_path(args):
    return "--config" in args or "-c" in args


def get_option_value(args, option_value_codes):
    """option_value_codes [short_option, long_option]"""
    for x in args:
        if x[0] == option_value_codes[0] or x[0] == option_value_codes[1]:
            if len(x[1]):
                return x[1]
            else: 
                print("Invalid option value")
                exit()

    return None


def has_required_options(args):
    counter = 0
    if is_export(args): counter += 1
    if is_import(args): counter += 1
    if is_add_config(args): counter += 1

    if counter > 1: 
        print("Can do only one of the following: --export, --import, --add")
        exit()

    if counter < 1:
        print("Requires one of the following: --export, --import, --add")
        exit()

    if has_config_path(args):
        return True

    return False


def get_option_codes(command_line_arguments):
    opts, values = zip(*command_line_arguments)
    return list(opts)


def parse_home_path(curr_path):
    if curr_path.find(getuser()) != -1 and not curr_path.startswith("~"):
        curr_path = curr_path[curr_path.find(getuser()):] 
        curr_path = curr_path[curr_path.find("/"):]
        curr_path = "~" + curr_path

    return curr_path


def get_new_config_file_details(new_config_file):
    offer_name = new_config_file.split("/")[-1]
    name = input("name [Default " + offer_name + "]: ")
    opt_dir = input("Sub directory [<Enter> for none]: ")
    details = [new_config_file]

    if not len(name): name = offer_name

    details.append(name)

    if len(opt_dir): details.append(opt_dir)

    return details


def process_args(args):
    if not len(args):
        print("-i or -e or -a plus -c are required arguments")

    short_opts, long_opts = get_option_definitions()
    try: 
        options = getopt.getopt(args, short_opts, long_opts) 
        option_codes = get_option_codes(options[0])
        required_options = has_required_options(option_codes)
        config_path = get_option_value(options[0], ["-c", "--config"])
        select_menu = is_select_menu(option_codes) 
        
        if required_options:
            if is_export(option_codes):
                exporter.export_configs(config_path, select_menu)
            elif is_import(option_codes): 
                importer.import_configs(config_path, select_menu) 
            elif is_add_config(option_codes):
                new_config_file = get_option_value(options[0], ["-a", "--add"])
                new_config_file = os.path.join(os.getcwd(), new_config_file)

                if not os.path.exists(new_config_file):
                    print("Could not resolve a path to the file")
                    exit()

                new_config_file = parse_home_path(new_config_file)
                config_details = get_new_config_file_details(new_config_file)

                exporter.add_new_config(config_details, config_path, select_menu)
        else: 
            print("-i or -e or -a plus -c are required arguments")
    except getopt.GetoptError as err:
        print(err)
        exit()
        

def get_option_definitions():
    short_options = "iea:sc:"
    long_options = [
                "import",
                "export",
                "add=",
                "select-menu",
                "config="
            ]

    return short_options, long_options


if __name__ == "__main__":
    process_args(argv[1:])
