#!/usr/bin/env python
# encoding: utf-8

"""
Script for managing modules listed in this directory. Modules should follow the
specifications written in the GUIDELINES.md file in this directory.

Usage:
    manage.py start [--no-daemon] [<module>...]
    manage.py stop [<module>...]

Options:
    -h, --help  Show this screen and exit.
"""

import os
import sys
import json
import docopt
import signal
from functools import wraps
import shlex, subprocess as sp

def get_module_info(module):
    with open(os.path.join(module, 'module.json'), 'r') as fp:
        return json.load(fp)

def get_pid_file(module):
    return os.path.join(module, 'module.pid')

def order_modules_by_dependencies(modules):
    """
    Dependency resolution algorithm, ordering the given modules by their
    dependencies. These ordered modules should be resolved in the returned
    order.
    """

    # build dependency mapping
    module_dependencies = {}
    for mod in modules:
        dependencies = get_module_info(mod).get('dependencies', [])
        for dep in dependencies:
            if dep not in modules:
                raise RuntimeError('Unknown dependency "%s"' % dep)
        module_dependencies[mod] = dependencies

    # dependency resolution
    ordered_modules = []
    resolved = set()
    resolving = set()
    def resolve_dependencies(module):
        if module in resolved:
            return
        resolving.add(module)
        for dep in module_dependencies[module]:
            if dep in resolving:
                raise RuntimeError('Circular dependency detected')
            resolve_dependencies(dep)
        resolved.add(module)
        ordered_modules.append(module)
        resolving.remove(module)

    # run dependency resolution
    for mod in module_dependencies.iterkeys():
        resolve_dependencies(mod)
    return ordered_modules

def needs_modules(f):
    """
    Decorator wrapping the query for modules for a function call, ensuring that
    a function needing them can access them with verifications made and
    defaulting to all the available modules. Uses the modules under the current
    directory.
    """
    @wraps(f)
    def inner(modules, *args, **kwargs):
        possible_modules = filter(os.path.isdir, os.listdir('.'))
        if len(modules) == 0 or modules is None:
            modules = possible_modules
        else:
            for mod in modules:
                if mod not in possible_modules:
                    raise RuntimeError('Unknown module "%s"' % mod)
        modules = order_modules_by_dependencies(modules)
        return f(modules, *args, **kwargs)
    return inner

@needs_modules
def start(modules, detach=False):
    """
    Start the modules given or all those under the current directory.
    """
    # check that the modules have not already been started
    for mod in modules:
        if os.path.exists(get_pid_file(mod)):
            raise RuntimeError('Module "%s"\'s pid file already exists' % mod)

    # start all modules
    this_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(os.path.join(this_dir, 'core')))
    module_procs = []
    for mod in modules:
        # get module start command
        try:
            command = get_module_info(mod)['start']
        except IOError as e:
            print 'error: "%s"' % str(e)
            continue

        # create module process
        print 'Starting module "%s" ...' % mod,
        os.chdir(mod)
        proc = sp.Popen(shlex.split(command), stdout=sp.PIPE, stderr=sp.PIPE)
        module_procs.append((mod, proc))
        os.chdir(this_dir)
        print 'done, pid:', proc.pid

    # handle exit
    if detach:
        for mod, proc in module_procs:
            with open(get_pid_file(mod), 'w') as fp:
                fp.write(str(proc.pid))
    else:
        def signal_handler(signal, frame):
                print 'Exit requested, terminating...'
                for mod, proc in module_procs:
                    print 'Terminating module "%s"' % mod
                    proc.terminate()
                sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        print 'Modules started: enter Ctrl-C to terminate all modules'
        signal.pause()

@needs_modules
def stop(modules):
    # check that the modules have already been started
    for mod in reversed(modules):
        print 'Stopping module "%s" ...' % mod,
        mod_pid_file = get_pid_file(mod)
        if not os.path.exists(mod_pid_file):
            print 'error: pid file doesn\'t exist'
            continue
        with open(mod_pid_file, 'r') as fp:
            mod_pid = int(fp.read().strip('\r\n'))
            try:
                os.kill(mod_pid, signal.SIGTERM)
            except OSError as e:
                print 'error: "%s"' % str(e)
                continue
            finally:
                os.remove(mod_pid_file)
        print 'done'

if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    # change to this directory (easier programming solution)
    this_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(this_dir)

    # handle arguments
    modules = args['<module>']
    try:
        if args['start']:
            detach = not args['--no-daemon']
            start(modules, detach)
        elif args['stop']:
            stop(modules)
    except RuntimeError as e:
        print 'Error: %s' % e
        sys.exit(1)
