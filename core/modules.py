import os
import json
import socket

_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
_modules_path = os.path.join(_root, 'modules')

CONFIG_FILE = 'module.json'
SOCKET_FILE = 'module.sock'

class DoesNotExist(Exception):
    """
    Custom exception raised when an operation requiring a module cannot be done
    because the module doesn't exist (bad module name for example).
    """
    def __init__(self, module_name):
        self.module_name = module_name

    def __str__(self):
        return 'Module "%s" does not exist' % self.module_name

def get_all():
    """
    Get all the modules available.
    """
    return [x for x in os.listdir(_modules_path) \
            if os.path.isdir(get_directory(x)) \
            and os.path.exists(get_config_file(x))]

def get_directory(module_name):
    """
    Get the absolute path to the directory for the given module.
    """
    return os.path.join(_modules_path, module_name)

def get_config_file(module_name):
    return os.path.join(get_directory(module_name), CONFIG_FILE)

def get_config(module_name):
    """
    Get the module's configuration, raising a DoesNotExist error if the given
    module doesn't exist.
    """
    try:
        with open(get_config_file(module_name)) as fp:
            return json.load(fp)
    except IOError:
        raise DoesNotExist(module_name)

def get_socket(module_name):
    """
    Get the module's corresponding socket. raising a DoesNotExist error if the
    given module doesn't exist.
    """
    conf = get_config(module_name)
    default_sockfile = os.path.join(get_directory(module_name), SOCKET_FILE)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    print default_sockfile
    sock.connect(conf.get('socket', default_sockfile))
    return sock
