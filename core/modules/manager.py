import threading
from .instances import Instance

def start_instance(instance_name, module_name, instance_kwargs={}, thread_kwargs={}):
    """
    Start a new instance of the module labeled as *module_name*, as an instance
    named by *instance_name*, passing *instance_kwargs* options. Returns a pair
    containing the instance launched and a Thread object (see threading.Thread
    for more details) corresponding to the launched instance. The thread is
    launched using *thread_kwargs* as kwargs.
    """
    instance = Instance(instance_name, module_name, **instance_kwargs)
    instance_thread = None # TODO
    return instance, instance_thread

def stop_instance(instance_name):
    """
    Stop the instance *instance_name*, raising a Instance.NotStarted if the
    instance isn't started.
    """
    pass
