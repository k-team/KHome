#!/usr/bin/env python2

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
