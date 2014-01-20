import os
import json
import socket
from . import get_config as get_module_config

_file = os.path.realpath(__file__)
_root = os.path.dirname(os.path.dirname(os.path.dirname(_file)))
_instances_dir = os.path.join(_root, 'instances')

class Instance(object):
    """
    Instance class, used to represent a launched module and its specific
    configuration, which is available prior to startup.
    """

    # default socket path relative to instance directory
    SOCKET_FILE = 'instance.sock'

    class Error(Exception):
        """
        Base class for all instance exceptions.
        """
        def __init__(self, instance):
            self.instance = instance

        def __str__(self):
            return 'Unspecified error for instance "%s" of module "%s"' % \
                    (self.instance.name, self.instance.module_name)

    class NotStarted(Error):
        """
        Exception raised when an instance isn't started.
        """

    class NotAvailable(Error):
        """
        Exception raised when an instance isn't available.
        """

    def __init__(self, name, module_name, **opts):
        """
        Build the instance passing its name, the module's name and the extra
        options to be applied over the module's default options.
        """
        self.name = name
        self.module_name = module_name
        self.opts = opts.update(get_module_config(module_name))

    @property
    def directory(self):
        """
        Path to the instance's directory.
        """
        return os.path.join(_instances_dir, self.name)

    @property
    def sockfile(self):
        """
        Get the instance's corresponding socket file, a file-like object linked
        to the instance's socket. Raises a NotAvailable error if the socket
        doesn't exist, which is probably due to the instance not being started.
        """
        try:
            default_sockfile = os.path.join(self.directory, self.SOCKET_FILE)
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(self.opts.get('socket', default_sockfile))
            return sock.makefile()
        except socket.error:
            raise self.NotAvailable(self)

def get_instance_directory(self, instance_name):
    return Instance(instance_name).directory

def get_instance_sockfile(self, instance_name):
    return Instance(instance_name).sockfile
