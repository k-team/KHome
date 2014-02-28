import os
import zipfile

import module.path as path
from module.packaging import (load_config, get_from_config, CONFIG_DEFAULTS,
        is_installed, MODULE_NAME_ENTRY)
_mne = MODULE_NAME_ENTRY

def get_zipfile(module_name):
    """
    Return the filename for the module's install zip.
    TODO make this more elegant (unify)
    """
    return os.path.join(path.availables_directory(), module_name + '.zip')

def is_available(module_name):
    """
    Return if the module named as *module_name* is available.
    """
    return module_name in (m[_mne] for m in get_available_modules())

def get_available_modules(detailed=False):
    """
    Return a list of all available modules. Detailed information can be given
    (eg. module configuration) by setting the "detailed" argument to true.
    """
    module_list = []
    dir_ = path.availables_directory()
    for module_fname in os.listdir(dir_):
        mod_full_dir = os.path.join(dir_, module_fname)
        if not module_fname.lower().endswith('.zip'):
            continue
        with zipfile.ZipFile(mod_full_dir) as zf:
            module_name = os.path.splitext(module_fname)[0]
            module_dir = module_name + '/'
            if module_dir not in zf.namelist():
                continue
            module_config_file = path.config_file(module_name,
                    directory=module_dir)
            with zf.open(module_config_file) as module_config_fp:
                conf = load_config(module_config_fp)
                if detailed:
                    conf['installed'] = is_installed(module_name)
                    module_list.append(conf)
                else:
                    module_list.append({ _mne: conf[_mne] })
    return module_list
