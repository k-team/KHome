import os
import json
import shlex
import shutil
import zipfile
import logging
import subprocess as sp

import path
import instance

logger = logging.getLogger(__name__)
def setup_logger(logger):
    logger.setLevel(logging.DEBUG)
    fmt = '%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s'
    formatter = logging.Formatter(fmt)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
setup_logger(logger)

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

def run_module_command(module_name, cmd):
    """
    Run a command listed in the "commands" section, for the module, other than
    "start" of course, which is a *special* command. Please note that the
    module should be trusted when running this command, otherwise bad stuff can
    happen. Return if the command was successful, or if there was no command to
    run (meaning that if no entry for that command is specified, this function
    returns true).
    """
    conf = get_config(module_name)
    if 'commands' not in conf or cmd not in conf['commands']:
        return True

    # run command
    ret = True
    cwd = os.getcwd()
    try:
        os.chdir(path.module_directory(module_name))
        log_file = open(path.log_file(module_name), 'a')
        sp.check_call(conf['commands'][cmd], stdout=log_file, stderr=log_file, shell=True)
    except (sp.CalledProcessError, OSError) as e:
        logger.exception(e)
        ret = False
    finally:
        log_file.close()
        os.chdir(cwd)
    return ret

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
        module_name = toplevel_directories[0][:-1]
        if is_installed(module_name):
            raise ValueError('Module already installed')

        # extract zip file
        zf.extractall(path.modules_directory())

    # run the "install" command
    if not run_module_command(module_name, 'install'):
        uninstall(module_name)
        return False

    # start the module
    instance.invoke(module_name)
    return True

def uninstall(module_name):
    """
    Uninstall a module by its name. Raise a ValueError if the module is already
    installed.
    """
    if not is_installed(module_name):
        raise ValueError('Module not installed')

    # stop the instance
    try:
        instance.stop(module_name)
    except RuntimeError:
        pass # ignore if module is already stopped

    # run the "uninstall" command
    # if not run_module_command(module_name, 'uninstall'):
    #     print 'Pas reussi a desinstaller'
    #     return False

    # remove the module directory tree
    try:
        shutil.rmtree(path.module_directory(module_name))
    except OSError as e:
        logger.exception(e)
        return False
    else:
        return True
