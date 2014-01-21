"""
Modules can be installed by copying their source directory under the `modules`
directory. The catalog handles installing modules from a zipfile, and updating
the module database at the same time.
"""

import os
import zipfile
#from . import get_directory, get_config

def get_installed_modules():
    return [x for x in os.listdir(DIRECTORY) \
            if os.path.isdir(get_directory(x)) \
            and os.path.exists(os.path.join(get_directory(x), CONFIG_FILE))]

def install_from_zip(filename):
    """
    Execute all the setup steps for a module installation.
    """
    pass

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
