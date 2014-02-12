import os
import sys
sys.path.append('./core')
import shlex
import signal
import daemon
import logging
import subprocess
from module import get_pid_file, get_module_directory
from catalog import get_config

# popen object containing the child
child_proc = None

def signal_handler(signum, frame):
    """
    Signal handler. If no child was created, it does nothing.
    Else, it broadcasts the signal to the child.
    """
    global child_proc
    logger = logging.getLogger()
    logger.info('Receive a signal ' + str(signum) + '. Broadcast it to the child')
    if child_proc is not None:
        child_proc.send_signal(signum)
        child_proc.wait()

def start_module(module_name, daemonize=True):
    """
    Start a new module identified by its name *module_name*.
    """
    global child_proc

    # Check that only one instance is running at the same time
    pid_file = get_pid_file(module_name)
    if os.path.exists(pid_file):
        raise RuntimeError('A pid file already exists for this module')
        sys.exit(1)

    # Get the start command from the configuration file
    module_config = get_config(module_name)
    if not 'start' in module_config:
        raise RuntimeError(
                'Missing start entry in the module\'s configuration file')
    start_cmd = module_config['start']

    # Daemon or not Daemon ?
    if daemonize:
        # Create a daemon
        daemon.possess_me()

        # Redirect stdout and stderr into a log file
        sys.stdout = open(pid_file + '.log', 'a')
        sys.stderr = sys.stdout

    # Create a logger and return it
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
            '%(asctime)s :: %(levelname)s :: %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    # Change the directory to the module directory
    os.chdir(get_module_directory(module_name))

    # Prepare to receive signal SIGINT and SIGTERM
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    return_code = 0
    try:
        # Write the new daemon pid in a new file
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))
            f.flush()
    except (OSError, IOError) as e:
        return_code = 1
    else:
        # Execute the start command
        logging.info('Start of the ' + module_name + ' module.')
        try:
            child_proc = subprocess.Popen(
                    shlex.split(start_cmd),
                    stdout=sys.stdout,
                    stderr=sys.stderr)
        except OSError as e:
            logging.exception(e)
            return_code = 1
        else:
            return_code = child_proc.wait()
    finally:
        # Remove the pid file and return the corresponding code
        logging.info('Shutdown of the ' + module_name + ' module.')
        os.remove(pid_file)
        sys.exit(return_code)

if __name__ == '__main__':
    # Get the module to launch
    try:
        module_name = sys.argv[1]
    except IndexError:
        sys.exit(1)

    daemonize = False

    start_module(module_name, daemonize)
