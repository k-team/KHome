#!/usr/bin/env python
# encoding: utf-8

"""
Script for managing modules listed in this directory. Modules should follow the
specifications written in the GUIDELINES.md file in this directory.

Todo:
- "install" command
- daemon (and no daemon) modes
- pid files

Usage:
    manage.py start [<module>...]
    manage.py install [<module>...]

Options:
    -h, --help  Show this screen and exit.
"""

import os
import sys
import json
import docopt
import signal
import subprocess as sp
import multiprocessing as mp

def install(modules=None):
    # TODO
    pass

def start(modules=None):
    """
    Start the modules given or all those under the current directory.
    """
    possible_modules = filter(os.path.isdir, os.listdir('.'))
    if len(modules) == 0 or modules is None:
        modules = possible_modules
    else:
        for mod in modules:
            if mod not in possible_modules:
                raise RuntimeError('Unknown module "%s"' % mod)

    # start all modules
    this_dir = os.getcwd()
    module_procs = []
    def run_module(command):
        return sp.call(command.split(), stdout=sp.PIPE, stderr=sp.PIPE)
    for mod in modules:
        print 'Starting module "%s" ...' % mod,
        os.chdir(mod)

        # load module start command from json file
        try:
            with open('module.json', 'r') as fp:
                command = json.load(fp)['start']
        except IOError as e:
            print 'error: "%s"' % str(e)
            continue

        # create module process
        proc = mp.Process(target=run_module, args=[command])
        proc.start()
        module_procs.append((mod, proc))
        os.chdir(this_dir)
        print 'done'

    # handle exit
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

if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    # change to this directory (easier programming solution)
    this_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(this_dir)

    # handle arguments
    modules = args['<module>']
    if args['start']:
        start(modules)
    elif args['install']:
        install(modules)
