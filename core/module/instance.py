import os
import sys
import time
import shlex
import signal
import daemon
import logging
import subprocess
import traceback
import module
import packaging
import path

logger = logging.getLogger(__name__)

def status(module_name):
    """
    Return the status of the module *module_name*
    A module is considered as running if its pid file exists.
    Return true if the module is running else false.
    """
    pid_file = path.pid_file(module_name)
    return os.path.exists(pid_file)

def status_all():
    """
    Return the status of all the installed modules. See the above function
    *status* for more details.
    Return a dictionary from name to status (as boolean).
    """
    modules = packaging.get_installed_modules()
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
        logger.info('Received signal %s, broadcasting it to child' % signum)
        if child_proc is not None:
            child_proc.send_signal(signum)
            child_proc.wait()

    # Check that only one instance is running at the same time
    pid_file = path.pid_file(module_name)
    if os.path.exists(pid_file):
        raise RuntimeError('A pid file already exists for this module')
        sys.exit(1)

    # Get the start command from the configuration file
    module_config = packaging.get_config(module_name)
    if not 'start' in module_config:
        raise RuntimeError(
                'Missing "start" entry in the module\'s configuration file')
        sys.exit(1)
    start_cmd = module_config['start']

    # Daemon or not Daemon ?
    if daemonize:
        # Create a daemon
        daemon.possess_me()

        # Redirect stdout and stderr into a log file
        sys.stdout = open(path.log_file(module_name), 'a')
        sys.stderr = sys.stdout

    # Change the directory to the module directory
    os.chdir(path.module_directory(module_name))

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
        logger.info('Start of the ' + module_name + ' module.')
        try:
            child_proc = subprocess.Popen(
                    shlex.split(start_cmd),
                    stdout=sys.stdout,
                    stderr=sys.stderr)
        except OSError as e:
            logger.exception(e)
            return_code = 1
        else:
            return_code = child_proc.wait()
    finally:
        # Remove the pid file and return the corresponding code
        logger.info('Shutdown of the ' + module_name + ' module.')
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
        raise RuntimeError('The module `' + module_name + '` is already running')
    pid = os.fork()
    if pid == 0: # Child side
        try:
            execm(module_name, daemonize)
        # handle raising SystemExit (code from Python's stdlib)
        except SystemExit as e:
            if not e.args:
                exitcode = 1
            elif isinstance(e.args[0], int):
                exitcode = e.args[0]
            else:
                sys.stderr.write(str(e.args[0]) + '\n')
                sys.stderr.flush()
                exitcode = 0 if isinstance(e.args[0], str) else 1
        except: # don't lose a possible exception traceback
            exitcode = 1
            traceback.print_exc()
        finally:
            sys.exit(exitcode)
    return pid

def invoke_all():
    """
    Invoke all installed modules as daemon. Doesn't check if the modules are
    correctly launch. Return the list of pid of the new processes.
    """
    modules = packaging.get_installed_modules()
    pids = []
    for name in modules:
        try:
            pid = invoke(name, True)
            time.sleep(0.1)
        except RuntimeError:
            traceback.print_exc()
        else:
            assert pid != 0
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
    pid_file = path.pid_file(module_name)
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
    modules = packaging.get_installed_modules()
    for name in modules:
        try:
            stop(name)
        except RuntimeError:
            pass # Ignore if we try to stop a stopped module
