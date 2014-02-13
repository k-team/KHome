from os.path import join
import re

_file = os.path.realpath(__file__)
_root = os.path.dirname(os.path.dirname(_file))

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
    # serveur de store pour récupérer les availables ?
    AVAILABLES_DIRECTORY = 'available_modules'
    return join(_root, AVAILABLES_DIRECTORY)

def modules_directory():
    """
    Get the absolute path to the sockets directory.
    """
    MODULES_DIRECTORY = 'modules'
    return join(_root, MODULES_DIRECTORY)

def instances_directory():
    """
    Get the absolute path to the sockets directory.
    """
    INSTANCES_DIRECTORY = 'instances'
    return join(_root, INSTANCES_DIRECTORY)

def pids_directory():
    """
    Get the absolute path to the sockets directory.
    """
    PIDS_DIRECTORY = 'pids'
    return join(instances_directory(), PIDS_DIRECTORY)

def sockets_directory():
    """
    Get the absolute path to the sockets directory.
    """
    SOCKET_DIRECTORY = 'socket'
    return join(instances_directory(), SOCKET_DIRECTORY)

def logs_directory():
    """
    Get the absolute path to the logs directory.
    """
    LOG_DIRECTORY = 'log'
    return join(instances_directory(), LOG_DIRECTORY)

def module_directory(module_name):
    """
    Get the absolute path to the module directory for the named module.
    """
    module_name = realname(module_name)
    return join(modules_directory(), module_name)

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

def config_file(module_name):
    """
    Get the absolute path to the configuration file for the named module.
    """
    CONFIG_FILE = 'module.json'
    return join(module_directory(module_name), CONFIG_FILE)
