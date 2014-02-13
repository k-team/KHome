from os.path import join, dirname, realpath
import re

_file = realpath(__file__)
_root = dirname(dirname(dirname(_file)))

AVAILABLES_DIRECTORY = 'available_modules'
MODULES_DIRECTORY = 'modules'
INSTANCES_DIRECTORY = 'instances'
PIDS_DIRECTORY = 'pid'
SOCKET_DIRECTORY = 'socket'
LOG_DIRECTORY = 'log'
CONFIG_FILE = 'module.json'

def realname(module_name):
    """
    Return the real name of a module. The real name of a modules
    is in lower snake_case.
    Transform a CamelCase name into snake_case name.
    """
    reg_first = re.compile(r'(.)([A-Z][a-z]+)')
    reg_all = re.compile(r'([a-z0-9])([A-Z])')
    s1 = reg_first.sub(r'\1_\2', module_name)
    return reg_all.sub(r'\1_\2', s1).lower()

def availables_directory():
    """
    Get the absolute path to the directory of available modules.
    """
    # NOTE utile pour le code ? Ne doit on pas demander au
    # serveur de store pour recuperer les availables ?
    return join(_root, AVAILABLES_DIRECTORY)

def modules_directory():
    """
    Get the absolute path to the sockets directory.
    """
    return join(_root, MODULES_DIRECTORY)

def instances_directory():
    """
    Get the absolute path to the sockets directory.
    """
    return join(_root, INSTANCES_DIRECTORY)

def pids_directory():
    """
    Get the absolute path to the sockets directory.
    """
    return join(instances_directory(), PIDS_DIRECTORY)

def sockets_directory():
    """
    Get the absolute path to the sockets directory.
    """
    return join(instances_directory(), SOCKET_DIRECTORY)

def logs_directory():
    """
    Get the absolute path to the logs directory.
    """
    return join(instances_directory(), LOG_DIRECTORY)

def module_directory(module_name, directory=None):
    """
    Get the absolute path to the module directory for the named module.
    """
    module_name = realname(module_name)
    if directory is None:
        return join(modules_directory(), module_name)
    return join(directory, module_name)

def pid_file(module_name):
    """
    Get the absolute path to the pid file for the named module.
    """
    module_name = realname(module_name)
    return join(pids_directory(), module_name + '.pid')

def socket_file(module_name):
    """
    Get the absolute path to the socket file for the named module.
    """
    module_name = realname(module_name)
    return join(sockets_directory(), module_name + '.sock')

def log_file(module_name):
    """
    Get the absolute path to the log file for the named module.
    """
    module_name = realname(module_name)
    return join(logs_directory(), module_name + '.log')

def config_file(module_name, directory=None):
    """
    Get the absolute path to the configuration file for the named module,
    optionally passing in the directory from which this file will be
    accessible.
    """
    if directory is None:
        return join(module_directory(module_name), CONFIG_FILE)
    return join(directory, CONFIG_FILE)
