import os
import path

def is_ready(module_name):
    """
    Return if the module *module_name* is ready.
    This is detected by watching the ready file of the module.
    """
    return os.path.exists(path.ready_file(module_name))
