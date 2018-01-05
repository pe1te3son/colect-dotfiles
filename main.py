#!python3
from sys import argv, exit
import getopt 
from lib import exporter, importer

def is_import(args):
    return "--import" in args or "-i" in args


def is_export(args):
    return "--export" in args or "-e" in args


def is_select_menu(args):
    return "--select-menu" in args or "-s" in args


def has_config_path(args):
    return "--path" in args or "-p" in args


def get_config_path(args):
    for x in args:
        if x[0] == "-p" or x[0] == "--path":
            if len(x[1]):
                return x[1]
            else: 
                print("Invalid path parameter")
                exit()


def has_required_options(args):
    if is_export(args) and is_import(args):
        print("Can not export and import at same time")
        exit()
        
    if is_export(args) or is_import(args):
        if has_config_path(args):
            return True

    return False


def get_option_codes(command_line_arguments):
    opts, values = zip(*command_line_arguments)
    return list(opts)


def process_args(args):
    if not len(args):
        print("-i or -e and -p are required arguments")

    short_opts, long_opts = get_option_definitions()
    try: 
        options = getopt.getopt(args, short_opts, long_opts) 
        option_codes = get_option_codes(options[0])
        required_options = has_required_options(option_codes)
        config_path = get_config_path(options[0])
        select_menu = is_select_menu(option_codes) 
        
        if required_options:
            if is_export(option_codes):
                exporter.export_configs(config_path, select_menu)
            else: 
                importer.import_configs(config_path, select_menu) 
        else: 
            print("-i or -e and -p are required arguments")
    except getopt.GetoptError as err:
        print(err)
        exit()
        

def get_option_definitions():
    short_options = "iesp:"
    long_options = [
                "import",
                "export",
                "select-menu",
                "path="
            ]

    return short_options, long_options


if __name__ == "__main__":
    process_args(argv[1:])
