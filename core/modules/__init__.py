import os
import json

_file = os.path.realpath(__file__)
_root = os.path.dirname(os.path.dirname(os.path.dirname(_file)))

DIRECTORY = os.path.join(_root, 'modules')
CONFIG_FILE = 'module.json'

def get_config_file(module_name, directory=None):
    """
    Get the absolute path to the configuration file for the named module,
    optionally passing in the directory from which this file will be
    accessible.
    """
    if directory is None:
        directory = os.path.join(DIRECTORY, module_name)
    return os.path.join(directory, CONFIG_FILE)

def load_config(file_):
    """
    Load the configuration for the named module, passing in either the absolute
    path to the config file or directly the file-like object.
    """
    if isinstance(file_, str):
        file_ = open(file_, 'r')
    return json.load(file_)

def get_config(module_name, directory=None):
    """
    Load the configuration for the named module, passing in the 'directory'
    argument with the same use as for get_config_file().
    """
    return load_config(get_config_file(module_name, directory))
