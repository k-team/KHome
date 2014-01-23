import json
import socket
import multiprocessing as mp

def start_instance(module_name, process_kwargs={}):
    """
    Start a new instance of the module named by *module_name*, raising a
    DoesNotExist if the module couldn't be found. Pass the process kwargs to
    the newly started process (see multiprocessing.Process for more details).
    Return the instance's id (handled here).
    Note that the module can be in configuration mode after this call, if any
    of its attributes aren't configured properly. See configure_instance for
    details on how to configure a module instance.
    """
    pass

def stop_instance(instance_id):
    """
    Stop the module instance identified by *instance_id*.
    """
    pass

def configure_instance(instance_id, **kwargs):
    """
    Configure the module instance identified by *instance_id* with the
    configuration given by this function's kwargs. A call to this function will
    be a blocking call, since a socket connection must me made in order to
    dialog correctly with the started module.
    """
    pass
