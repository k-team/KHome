import os
import sys
import json
import time
import socket
import select
import logging
import threading
from twisted.internet import reactor
from twisted.internet.endpoints import UNIXServerEndpoint as ServerEndpoint

import path
import remote
import connection
import instance
import khome.fields

__all__ = ('path', 'connection', 'instance', 'remote',
        'Abstract', 'Base', 'Network', 'use_module', 'is_ready')

_launched_modules = []

class Abstract(threading.Thread):
    """
    Module class containing all further informations about a module. A module
    contains a list of fields. Each fields is a subthread of the module which
    is also a thread.
    """

    SUCCESS_EXIT = 0
    DEADFIELD_EXIT = 1
    JOIN_TIMEOUT = 5

    def __init__(self, name, socket_file, fields):
        """
        Construct the module with its *name*, and its *fields*. Also try to
        create a socket unix server endpoint on *socket_file* path.
        """
        threading.Thread.__init__(self)
        self.name = name
        self.fields = fields
        self.ready_file = path.ready_file(self.name)
        self.exitcode = self.SUCCESS_EXIT
        if os.path.exists(socket_file):
            os.remove(socket_file)
        endpoint = ServerEndpoint(reactor, socket_file)
        endpoint.listen(connection.Factory(self))

    def on_init(self):
        """
        Method calls before the start of the module's thread.
        """
        pass

    def on_stop(self):
        """
        Method calls after the execution of the module.
        """
        pass

    def identity(self):
        """
        Return a dictionary containing all informations about
        the module.
        """
        ans = {}
        ans['name'] = self.name
        ans['fields'] = {}
        for f in self.fields:
            info = f.get_info()
            if info:
                ans['fields'][f.name] += [info]
        return ans

    def start(self):
        """
        Start all fields of the module and then start itself.

        If it is ill-formed, raise a RuntimeError. Else, the module calls its
        on_init() method to let the module prepares itself before the start.
        Then, it starts all fields thread one after one and waits until the end
        of the startup of the field before continue. If one field doesn't start
        properly, the module stops all its running fields thread and raises a
        RuntimeError. When all fields are started, the module calls their
        on_start() method. After that, the module starts its own thread and
        indicates that it is ready.
        """
        self.on_init()
        self.start_fields()
        for f in self.fields:
            f.on_start()
        threading.Thread.start(self)
        self.is_ready = True

    def run(self):
        """
        Main function of the thread. Check if all the fields are alive. If one
        is dead, stop the execution of the module and set the exitcode to
        DEADFIELD_EXIT
        """
        while self.is_ready and all((f.isAlive() for f in self.fields)):
            time.sleep(0.1)

        if self.is_ready:
            self.exitcode = self.DEADFIELD_EXIT
        self.stop_fields()
        self.on_stop()

    def stop(self):
        """
        Stop the execution of the module and indicate that the
        module isn't ready anymore.
        """
        self.is_ready = False

    def start_fields(self):
        """
        Try to start all the fields of the module.

        Start each fields one after one and wait until each fields are ready.
        If one doesn't start properly, it raises a RuntimeError.
        """
        for field in self.fields:
            field.start()
            while not field.is_ready():
                time.sleep(0.05)
                if not field.isAlive():
                    self.stop_fields()
                    raise RuntimeError('Impossible to start %s' % repr(field))

    def stop_fields(self):
        """
        Stop all started fields.

        Join all fields' thread with a timeout of JOIN_TIMEOUT.
        Return True if of threads are joined, else False.
        """
        for field in self.fields:
            field.stop()
            field.join(self.JOIN_TIMEOUT)
        return not any((f.isAlive() for f in self.fields))

    @property
    def is_ready(self):
        """
        Indicate if the module is ready or not.

        A module is considered ready if all its fields are ready and it execute
        its startup on_init() method. It creates or removes a file to indicate
        to other remote module its state.
        """
        return remote.is_ready(self.name)

    @is_ready.setter
    def is_ready(self, value):
        if value:
            if os.path.exists(self.ready_file):
                os.remove(self.ready_file)
            fd = os.open(self.ready_file, os.O_CREAT, 0444)
            os.close(fd)
        else:
            os.remove(self.ready_file)

def kill():
    """
    Call the *stop()* function of all module running in this processus.
    Raise a runtime error.
    """
    for mod in _lauched_modules:
        logger.info('Killing module `%s`.', mod)
        mod.stop()
    raise RuntimeError('Application killed, cannot supply dependencies')

def prop_field(field):
    """
    Access the value of the field named as *field*. The access is done
    either in read or write mode depending on the parameters.

    Several cases are handled, given the parameters of the call:
    - none: return the last value saved
    - *t*: return the value whose saved time is nearest
    - *fr* and *to*: return all the values saved in the interval [fr, to]
    - unnamed: add a new value and return if it was successful
    """
    def _prop_field(*args, **kwargs):
        if len(args) == 1 and not kwargs:
            return field.write(*args)
        elif not args:
            if not kwargs:
                return field.read()
            if len(kwargs) == 1 and 't' in kwargs:
                return field.read(**kwargs)
            if len(kwargs) == 1 and 'update' in kwargs:
                return field.update()
            if len(kwargs) == 2 and 'fr' in kwargs and 'to' in kwargs:
                return field.read(**kwargs)
        raise ValueError("Field isn't specified correctly")
    return _prop_field

class BaseMeta(type):
    """
    Metaclass for building a module based on a module-like class.
    """
    def __new__(cls, name, parents, attrs):
        from khome.fields import Base as Field
        fields = []
        for f_cls in attrs.itervalues():
            if isinstance(f_cls, type) and issubclass(f_cls, Field):
                field = f_cls()
                attrs[field.field_name] = prop_field(field)
                fields.append(field)
        attrs['__fields__'] = fields
        return super(BaseMeta, cls).__new__(cls, name, parents, attrs)

    def __call__(self, *args, **kwargs):
        obj = super(BaseMeta, self).__call__(*args, **kwargs)
        _launched_modules.append(obj)
        return obj

class Base(Abstract):
    """
    Base module, subclass this if only core module functionalities are needed.
    """
    __metaclass__ = BaseMeta

    class Field(khome.fields.Base):
        pass

    def __init__(self):
        name = type(self).__name__
        fields = type(self).__fields__
        for f in fields:
            f.module = self
        Abstract.__init__(self, name, path.socket_file(name), fields)
