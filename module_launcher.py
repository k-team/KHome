#!/usr/bin/env python2

"""
Launch a python module.
The module has to be construct like this scheme :
    modules/
        module_name/
            module.json
            __main__.py => module_launcher (this file)
            module_name.py

The module_name.py file has to contains a module_name class which
is a module class.
"""

import os
import sys
from twisted.internet import reactor

module_dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(module_dirname, '../../core/'))
module_name = os.path.basename(module_dirname)

# Let the program stop if there is an error
module = __import__(module_name)
module_cls = getattr(module, module_name)
instance = module_cls()
instance.start()
reactor.run()
instance.stop()
instance.join(1)
