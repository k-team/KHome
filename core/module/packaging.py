import os
import json
import zipfile

import module.path as path

MODULE_NAME_ENTRY = 'name'

CONFIG_DEFAULTS = {
        'public_directory': 'public',
        'icon_name': 'icon.png',
        'partial_name': 'partial.html',
        'has_view': False
        }

def load_config(file_):
    """
    Load the configuration for the named module, passing in either the absolute
    path to the config file or directly the file-like object.
    """
    if isinstance(file_, (str, unicode)):
        file_ = open(file_, 'r')
    return json.load(file_)

def get_config(module_name, directory=None):
    """
    Load the configuration for the named module, passing in the 'directory'
    argument with the same use as for get_config_file().
    """
    return load_config(path.config_file(module_name, directory))

def get_from_config(conf, entry_name):
    return conf.get(entry_name, CONFIG_DEFAULTS[entry_name])

def is_installed(module_name, directory=None):
    """
    Return if the named module exists in the given directory (defaults to
    module installation directory).
    """
    module_directory = path.module_directory(module_name, directory)
    config_file = path.config_file(module_name, module_directory)
    return os.path.isdir(module_directory) and os.path.exists(config_file)

def get_installed_modules(detailed=False):
    """
    Return a list of all installed modules in the installation directory.
    Detailed information can be given (eg. module configuration) by setting the
    "detailed" argument to true.
    """
    module_list = []
    for module_name in os.listdir(path.modules_directory()):
        if not is_installed(module_name):
            continue
        if detailed:
            module_config = get_config(module_name)
            module_name = { MODULE_NAME_ENTRY: module_name }
            module_name.update(module_config)
        module_list.append(module_name)
    return module_list

def install_from_zip(file_):
    """
    Execute all the setup steps for a module installation. Takes either a
    filename or a file-like object (which should already be opened).
    Raises an IOError if the zip file reading failed, and a ValueError if the
    module is already installed.
    """
    with zipfile.ZipFile(file_) as zf:
        toplevel_directories = [n for n in zf.namelist() \
                if n.endswith('/') and n.count('/') == 1]

        # validate zip format
        if len(toplevel_directories) != 1:
            msg = 'Archive should only have one directory at its root'
            raise IOError(msg)

        # validate against already installed modules
        if is_installed(toplevel_directories[0][:-1]):
            raise ValueError('Module already installed')

        # extract zip file
        zf.extractall(path.modules_directory())
