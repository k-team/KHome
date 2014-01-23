"""
Modules can be installed by copying their source directory under the `modules`
directory. The catalog handles installing modules from a zipfile, and updating
the module database at the same time.
"""

import os
import json
import zipfile

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

def get_installed_modules():
    """
    Return a list of all installed modules in the installation directory.
    """
    return [x for x in os.listdir(DIRECTORY) if is_installed(x)]

def install_from_zip(file_):
    """
    Execute all the setup steps for a module installation. Takes either a
    filename or a file-like object (which should already be opened).
    """
    if isinstance(file_, str):
        file_ = open(file_, 'r')
    print load_config(file_.open(CONFIG_FILE, 'r'))

def unzip(source_filename, dest_dir):
    """
    Secure unzip method, copied from
    http://stackoverflow.com/a/12886818
    """
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''):
                    continue
                path = os.path.join(path, word)
            zf.extract(member, path)
