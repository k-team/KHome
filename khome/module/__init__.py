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

_file = os.path.realpath(__file__)
_root = os.path.dirname(os.path.dirname(os.path.dirname(_file)))

logger = logging.getLogger(__name__)

# launched modules for the current process
_launched_modules = []

SOCKET_TIMEOUT = 3

def kill():
    """
    Call the *stop()* function of all module running in this processus.
    Raise a runtime error.
    """
    for mod in _lauched_modules:
        logger.info('Killing module `%s`.', mod)
        mod.stop()
    raise RuntimeError('Application killed, cannot supply dependencies')

def get_socket(module_name, nb_try=5):
    """
    Return a socket connected to the module named *module_name*.
    The socket is transformed by the makefile function and has to be use as a
    file object.
    """
    for i in xrange(nb_try):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(path.socket_file(module_name))
        except socket.error as e:
            logger.exception(e)
            logger.error('Cannot connect to `%s` module. (%d / %d)',
                    module_name, i + 1, nb_try)
            time.sleep(0.5)
        else:
            return sock.makefile('rw')
    logger.error('Cannot connect to `%s` module.', module_name)
    return kill()

def network_write(conn, data):
    """
    Write *data* to the *conn* file, add a new line character at
    the end and flush the buffer output.
    Wait a maximum *SOCKET_TIMEOUT* sec for writing. If there is a
    timeout, modules are killed.
    When there is a IOError exception, modules are also killed.
    """
    _, wl, _ = select.select([], [conn], [], SOCKET_TIMEOUT)
    if not wl:
        raise RuntimeError('Cannot write to module.')
    conn = wl[0]
    try:
        conn.write(data + '\n')
        conn.flush()
    except IOError:
        return None
        return kill()

def network_readline(conn):
    """
    Read a entire line from the *conn* file.
    Wait a maximum of *SOCKET_TIMEOUT* sec for reading. If there
    is a timeout, modules are killed.
    When there is a IOError exception, modules are also killed.
    """
    rl, _, _ = select.select([conn], [], [], SOCKET_TIMEOUT)
    if rl is []:
        return None
        return kill()
    try:
        return json.loads(conn.readline())
    except (IOError, ValueError) as e:
        logger.exception(e)
        logger.error('Cannot read from module')
        # return kill()
    except TypeError as e:
        logger.exception(e)
        logger.error('Module sent bad data')
        return {}

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

def get_network_info(module_conn):
    """
    Return the list of the fields of a module connected through the
    *module_conn* file socket.
    """
    # TODO
    request = {}
    request['code'] = 'knockknock'
    network_write(module_conn, json.dumps(request))
    ans = network_readline(module_conn)
    return ans

def prop_network_field(module_conn, field_info):
    """
    Access the value of the field named as *field* inside a external module
    connected through the *module_conn* file socket. The access is done either in
    read or write mode depending on the parameters (same as prop_field, but
    through socket connection).
    """
    field_name = field_info['name']
    def _prop_network_field(*args, **kwargs):
        if len(args) == 1 and not kwargs:
            request = {}
            request['code'] = 'set'
            request['field_name'] = field_name
            request['field_value'] = args[0]
            network_write(module_conn, json.dumps(request))
            ans = network_readline(module_conn)
            if ans is not None:
                return ans.get('success', False)
            return None
        elif not args:
            if not kwargs:
                request = {}
                request['code'] = 'get'
                request['fields'] = [field_name]
            if len(kwargs) == 1 and 't' in kwargs:
                request = {}
                request['code'] = 'get_at'
                request['time'] = time.time() + kwargs['t']
                request['fields'] = [field_name]
            if len(kwargs) == 2 and 'fr' in kwargs and 'to' in kwargs:
                request = {}
                request['code'] = 'get_from_to'
                request['time_from'] = time.time() + kwargs['fr']
                request['time_to'] = time.time() + kwargs['to']
                request['fields'] = [field_name]

            network_write(module_conn, json.dumps(request))
            ans = network_readline(module_conn)

            if not ans.get('success', False):
                return None
            try:
                return ans['fields'][field_name]
            except KeyError:
                return None
        raise ValueError("Field isn't specified correctly")
    return _prop_network_field

class BaseMeta(type):
    """
    Metaclass for building a module based on a module-like class.
    """
    ls_name = set()

    def __new__(cls, name, parents, attrs):
        print attrs
        # Handle module fields
        # from khome.fields import Base as Field
        # for f_cls in cls.__dict__.keys():
        #     f_cls = getattr(cls, f_cls)
        #     if isinstance(f_cls, type) and issubclass(f_cls, Field):
        #         field = f_cls()
        #         setattr(obj, field.field_name, prop_field(field))
        #         setattr(field, 'module', obj)
        #         ls_fields += [field]
        # setattr(obj, 'module_fields', ls_fields)

        return super(BaseMeta, cls).__new__(cls, name, parents, attrs)

    def __call__(self, *args, **kwargs):
        obj = super(BaseMeta, self).__call__(*args, **kwargs)
        cls = type(obj)

        _lauched_modules.append(obj)
        return obj

class NetworkMeta(type):
    """
    Metaclass for building network-interfaced modules, the same way BaseMeta
    builds modules.
    """
    def __new__(cls, name, parents, attrs):
        return super(NetworkMeta, cls).__new__(cls, name, parents, attrs)

    def __call__(self, *args, **kwargs):
        obj = super(NetworkMeta, self).__call__(*args, **kwargs)
        cls = type(obj)

        # Gestion du nom du module
        if not hasattr(obj, 'module_name'):
            if not hasattr(cls, 'module_name'):
                setattr(obj, 'module_name', cls.__name__)
            else:
                setattr(obj, 'module_name', cls.module_name)

        # Gestion de la connection au module
        conn = get_socket(obj.module_name)
        setattr(obj, 'module_conn', conn)

        # Gestion des fields du module
        info = get_network_info(conn)
        setattr(obj, 'info', info)
        fields = info['fields']
        fields_info = {}
        for field in fields:
            fields_info[field['name']] = field
            setattr(obj, field['name'], prop_network_field(conn, field))
        setattr(obj, 'fields_info', fields_info)

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
        Abstract.__init__(self, name, path.socket_file(name), [])

class Network(object):
    """
    Network module base, built just like Base module, but with network
    interfacing.
    """
    __metaclass__ = NetworkMeta

    def __init__(self, **kwargs):
        super(Network, self).__init__()
        _setup_module(self, **kwargs)

def _setup_module(obj, **kwargs):
    """
    Refactoring for initializing operations for module classes.
    """
    if 'name' in kwargs:
        obj.module_name = kwargs['name']

def use_module(module_name):
    """
    Shortcut for referencing a module through network, given its module name.
    """
    name = path.realname(module_name)
    if not instance.status(name):
        logging.info('Trying to launch the `%s` dependancy module.',
                module_name)
        instance.invoke(name, True)
        t = time.time()
        while not remote.is_ready(module_name):
            time.sleep(0.1)
            if time.time() - t > SOCKET_TIMEOUT:
                logging.error('Cannot launch the `%s` dependency: abort',
                        module_name)
                return kill()
        logging.info('`%s` dependancy module successfully launched.',
                module_name)
    return Network(name=module_name)
