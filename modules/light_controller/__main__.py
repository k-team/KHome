#!/usr/bin/env python2

"""
Launch a python module.
The module has to be construct like this scheme :
    modules/
        module_name/
            module.json
            __main__.py => module_launcher (this file)
            local_module.py

The module_name.py file has to contains a module_name class which
is a module class.
"""

import os
import sys
from twisted.internet import reactor

module_dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(module_dirname, '../../core/'))
import module
import local_module

for _, value in local_module.__dict__.items():
    try:
        if issubclass(value, module.Base):
            module_cls = value
            break
    except TypeError:
        pass

instance = module_cls()
instance.start()
reactor.run()
instance.stop()
instance.join(1)
