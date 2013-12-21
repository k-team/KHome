#!/usr/bin/env python
# encoding: utf-8

"""
Usage:
    manage.py (start|install)

Options:
    -h, --help  Show this screen and exit.
"""

from docopt import docopt

def start():
    print 'Starting'

def install():
    print 'Installing'

if __name__ == '__main__':
    args = docopt(__doc__)
    if args['start']:
        start()
    elif args['install']:
        install()
