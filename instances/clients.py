#!/usr/bin/env python
# encoding: utf-8

"""
Script for managing client instances listed in this directory.

Usage:
    clients.py start [--no-daemon] [<client>...]
    clients.py stop [<client>...]

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

this_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(this_dir)
clients_dir = os.path.join(root_dir, 'clients')
core_dir = os.path.join(root_dir, 'core')

def get_client_info(client):
    with open(os.path.join(client, 'client.json'), 'r') as fp:
        return json.load(fp)

def get_pid_file(client):
    return os.path.join(client, 'client.pid')

def start(clients, detach=False):
    """
    Start the clients given or all those under the client directory.
    """
    # check that the clients have not already been started
    for client in clients:
        if os.path.exists(get_pid_file(client)):
            raise RuntimeError('Client "%s"\'s pid file already exists' % client)

    # start all clients
    client_procs = []
    env = { 'PYTHONPATH': core_dir }
    for clien in clients:
        # get client start command
        try:
            command = get_client_info(client)['start']
        except IOError as e:
            print 'error: "%s"' % str(e)
            continue

        # create client process
        print 'Starting client "%s" ...' % client,
        os.chdir(client)
        proc = sp.Popen(shlex.split(command), env=env,
                stdout=sp.PIPE, stderr=sp.PIPE)
        client_procs.append((client, proc))
        os.chdir(clients_dir)
        print 'done, pid:', proc.pid

    # handle exit
    if detach:
        for client, proc in client_procs:
            with open(get_pid_file(client), 'w') as fp:
                fp.write(str(proc.pid))
    else:
        def signal_handler(signal, frame):
                print 'Exit requested, terminating...'
                for client, proc in client_procs:
                    print 'Terminating client "%s"' % client
                    proc.terminate()
                sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        print 'Clients started: enter Ctrl-C to terminate all clients'
        signal.pause()

def stop(clients):
    # check that the clients have already been started
    for client in clients:
        print 'Stopping client "%s" ...' % client,
        client_pid_file = get_pid_file(client)
        if not os.path.exists(client_pid_file):
            print 'error: pid file doesn\'t exist'
            continue
        with open(client_pid_file, 'r') as fp:
            client_pid = int(fp.read().strip('\r\n'))
            try:
                os.kill(client_pid, signal.SIGTERM)
            except OSError as e:
                print 'error: "%s"' % str(e)
                continue
            finally:
                os.remove(client_pid_file)
        print 'done'

if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    # change to client directory (easier programming solution)
    os.chdir(clients_dir)

    # handle arguments
    clients = args['<clients>']
    try:
        if args['start']:
            detach = not args['--no-daemon']
            start(clients, detach)
        elif args['stop']:
            stop(clients)
    except RuntimeError as e:
        print 'Error: %s' % e
        sys.exit(1)
