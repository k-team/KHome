import os
import sys
import shlex
import signal
import daemon
import logging
import subprocess
import module
import catalog

def status(module_name):
    """
    Return the status of the module *module_name*
    A module is considered as running if its pid file exists.
    Return true if the module is running else false.
    """
    pid_file = module.get_pid_file(module_name)
    return os.path.exists(pid_file)

def status_all():
    """
    Return the status of all the installed modules. See the above function
    *status* for more details.
    Return a dictionary from name to status (as boolean).
    """
    modules = catalog.get_installed_modules()
    return {name: status(name) for name in modules}

def execm(module_name, daemonize=True):
    """
    Start a new module identified by its name *module_name*. The current
    processus is killed at the end of the module when it's not a daemon. If it
    is, the current processus is killed immediately. Use *invoke*
    instead if you want to create a new killable process.
    """
    child_proc = None

    def signal_handler(signum, frame):
        """
        Signal handler. If no child was created, it does nothing.
        Else, it broadcasts the signal to the child.
        """
        logger = logging.getLogger()
        logger.info('Receive a signal ' + str(signum) + '. Broadcast it to the child')
        if child_proc is not None:
            child_proc.send_signal(signum)
            child_proc.wait()

    # Check that only one instance is running at the same time
    pid_file = module.get_pid_file(module_name)
    if os.path.exists(pid_file):
        raise RuntimeError('A pid file already exists for this module')
        sys.exit(1)

    # Get the start command from the configuration file
    module_config = catalog.get_config(module_name)
    if not 'start' in module_config:
        raise RuntimeError(
                'Missing start entry in the module\'s configuration file')
        sys.exit(1)
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
    os.chdir(module.get_module_directory(module_name))

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
    sys.exit(0)

def invoke(module_name, daemonize=True):
    """
    As exec_module, execute a module but fork before to keep the current
    process active. To see if the module is really running, use the
    *status* function.
    Return the new process's pid. In case of error, return 0.
    """
    if status(module_name):
        raise RuntimeError('The module is already running')
        return 0
    try:
        pid = os.fork()
    except OSError as e:
        raise e
        return 0
    else:
        if pid == 0: # Child side
            execm(module_name, daemonize)
            sys.exit(0)
        else: # Parent side
            return pid
    return 0

def invoke_all():
    """
    Invoke all installed modules as daemon. Doesn't check if the modules are
    correctly launch. Return the list of pid of the new processes.
    """
    modules = catalog.get_installed_modules()
    pids = []
    for name in modules:
        if not status(name):
            pid = invoke(name, True)
            if pid != 0:
                pids.append(pid)
    return pids

def stop(module_name):
    """
    Stop the *module_name* module.
    """
    if not status(module_name):
        raise RuntimeError('The module `' + module_name + '`is not running')

    remove_file = False
    pid = 0
    pid_file = module.get_pid_file(module_name)
    with open(pid_file, 'r') as f:
        try:
            pid = int(f.readline())
        except ValueError:
            remove_file = True

    if pid != 0:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as e:
            if e.errno == 3: # No such process
                remove_file = True
            else:
                raise e

    if remove_file:
        os.remove(pid_file)

def stop_all():
    """
    Stop all the running modules
    """
    modules = catalog.get_installed_modules()
    for name in modules:
        try:
            stop(name)
        except RuntimeError:
            pass # Ignore if we try to stop a stopped module
