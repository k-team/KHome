"""
Modules can be installed by copying their source directory under the `modules`
directory. The catalog handles installing modules from a zipfile, and updating
the module database at the same time.
"""

import os
import json
import zipfile

import module
import module.path as path

_file = os.path.realpath(__file__)
_root = os.path.dirname(os.path.dirname(_file))

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

def is_installed(module_name, directory=None):
    """
    Return if the named module exists in the given directory (defaults to
    module installation directory).
    """
    module_directory = path.module_directory(module_name, directory)
    config_file = path.config_file(module_name, module_directory)
    return os.path.isdir(module_directory) and os.path.exists(config_file)

def is_available(module_name):
    """
    Return if the module named as *module_name* is available.
    """
    return module_name in (m['id'] for m in get_available_modules())

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
            module_name = { 'id': module_name }
            module_name.update(module_config)
        module_list.append(module_name)
    return module_list

def get_available_modules(detailed=False):
    """
    Return a list of all available modules. Detailed information can be given
    (eg. module configuration) by setting the "detailed" argument to true.
    """
    module_list = []
    dir_ = path.availables_directory()
    for module_name in os.listdir(dir_):
        mod_full_dir = os.path.join(dir_, module_name)
        if not module_name.lower().endswith('.zip'):
            continue
        with zipfile.ZipFile(mod_full_dir) as zf:
            module_dir = os.path.splitext(module_name)[0] + '/'
            if module_dir not in zf.namelist():
                continue
            module_config_file = path.config_file(
                    module_name, directory=module_dir)
            with zf.open(module_config_file) as module_config_fp:
                conf = load_config(module_config_fp)
                if detailed:
                    module_list.append({ 'id': conf['id'] })
                else:
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
            path = path.modules_directory()
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''):
                    continue
                path = os.path.join(path, word)
            zf.extract(zi, path)

        # TODO start module ?
