import os
import path

def is_ready(module_name):
    return os.path.exists(path.ready_file(module_name))
