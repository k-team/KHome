"""
Test a module with this script

Usage:
    test_module <module_name>
"""
import os
import sys
import docopt

sys.path.append('core')
from module import use_module

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    module_name = args['<module_name>']
    mod = use_module(module_name)

    # fields
    fields = mod.info['fields']
    if fields:
        print 'Fields:'
    for field in fields:
        get = getattr(mod, field['name'])
        print '-', field['name'], ':', field['type'], '(current value = %s)' % get()

