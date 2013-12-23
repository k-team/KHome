#!/usr/bin/env python
# encoding: utf-8

"""
Script for managing modules listed in this directory. Modules should follow the
specifications written in the GUIDELINES.md file in this directory.

Todo:
- "install" command
- "start" command dependencies
- daemon (and no daemon) modes
- pid files

Usage:
    manage.py start [--no-daemon] [<module>...]
    manage.py stop [<module>...]
    manage.py install [<module>...]

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
        return f(modules, *args, **kwargs)
    return inner

def get_module_info(module):
    with open(os.path.join(module, 'module.json'), 'r') as fp:
        return json.load(fp)

def get_pid_file(module):
    return os.path.join(module, 'module.pid')

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
    this_dir = os.getcwd()
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
    for mod in modules:
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

@needs_modules
def install(modules):
    # TODO
    pass

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
        elif args['install']:
            install(modules)
    except RuntimeError as e:
        print 'Error: %s' % e
        sys.exit(1)
