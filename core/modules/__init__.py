import os

# Currently, modules are directories under the "modules" directory. This should
# be replaced in the future by a database with a catalog of modules.

_file = os.path.realpath(__file__)
_root = os.path.dirname(os.path.dirname(os.path.dirname(_file)))
_modules_path = os.path.join(_root, 'modules')

CONFIG_FILE = 'module.json'

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
    Get a list of all the available modules.
    """
    return [x for x in os.listdir(_modules_path) \
            if os.path.isdir(get_directory(x)) \
            and os.path.exists(os.path.join(get_directory(x), CONFIG_FILE))]

def get_directory(module_name):
    """
    Get the absolute path to the directory for the given module.
    """
    return os.path.join(_modules_path, module_name)

def get_config(module_name):
    config_file = os.path.join(get_directory(module_name), CONFIG_FILE)
    try:
        with open(config_file, 'r') as fp:
            return json.load(fp)
    except IOError:
        raise DoesNotExist(module_name)
