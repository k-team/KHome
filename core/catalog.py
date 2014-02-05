"""
Modules can be installed by copying their source directory under the `modules`
directory. The catalog handles installing modules from a zipfile, and updating
the module database at the same time.
"""

import os
import json
import zipfile

from module import get_directory, DIRECTORY

_file = os.path.realpath(__file__)
_root = os.path.dirname(os.path.dirname(_file))

AVAILABLE_DIRECTORY = os.path.join(_root, 'available_modules')
CONFIG_FILE = 'module.json'

def get_config_file(module_name, directory=None):
    """
    Get the absolute path to the configuration file for the named module,
    optionally passing in the directory from which this file will be
    accessible.
    """
    if directory is None:
        directory = get_directory(module_name)
    return os.path.join(directory, CONFIG_FILE)

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
    return load_config(get_config_file(module_name, directory))

def is_installed(module_name, directory=None):
    """
    Return if the named module exists in the given directory (defaults to
    module installation directory).
    """
    if directory is None:
        directory = DIRECTORY
    module_directory = os.path.join(directory, module_name)
    return os.path.isdir(module_directory) \
            and os.path.exists(get_config_file(module_name, module_directory))

def get_installed_modules(detailed=False):
    """
    Return a list of all installed modules in the installation directory.
    Detailed information can be given (eg. module configuration) by setting the
    "detailed" argument to true.
    """
    module_list = []
    for module in os.listdir(DIRECTORY):
        if not is_installed(module):
            continue
        if detailed:
            module_config = get_config(module)
            module = { 'id': module }
            module.update(module_config)
        module_list.append(module)
    return module_list

def get_available_modules(detailed=False):
    """
    Return a list of all available modules. Detailed information can be given
    (eg. module configuration) by setting the "detailed" argument to true.
    """
    module_list = []
    dir_ = AVAILABLE_DIRECTORY
    for module in os.listdir(dir_):
        mod_full_dir = os.path.join(dir_, module)
        if not module.lower().endswith('.zip'):
            continue
        with zipfile.ZipFile(mod_full_dir) as zf:
            module_dir = os.path.splitext(module)[0] + '/'
            if module_dir not in zf.namelist():
                continue
            module_config_file = get_config_file(module, directory=module_dir)
            with zf.open(module_config_file) as module_config_fp:
                conf = load_config(module_config_fp)
                module_list.append(conf)
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
        for zi in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = zi.filename.split('/')[1:]
            path = DIRECTORY
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''):
                    continue
                path = os.path.join(path, word)
            zf.extract(zi, path)

        # TODO start module ?
