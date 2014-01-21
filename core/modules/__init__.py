import os

_file = os.path.realpath(__file__)
_root = os.path.dirname(os.path.dirname(os.path.dirname(_file)))

DIRECTORY = os.path.join(_root, 'modules')
CONFIG_FILE = 'module.json'

def get_directory(module_name):
    """
    Get the absolute path to the directory for the given module.
    """
    return os.path.join(DIRECTORY, module_name)

def get_config(module_name):
    config_file = os.path.join(get_directory(module_name), CONFIG_FILE)
    with open(config_file, 'r') as fp:
        return json.load(fp)
