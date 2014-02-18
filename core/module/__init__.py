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

import fields
from . import connection
import path
import instance

_file = os.path.realpath(__file__)
_root = os.path.dirname(os.path.dirname(os.path.dirname(_file)))

SOCKET_TIMEOUT = 10

_running_modules = []

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
        '%(asctime)s :: %(levelname)s :: %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

def kill():
    """
    Call the kill function of all running in this proc.
    Raise a runtime error.
    """
    logger = logging.getLogger()
    logger.info('Application killed')
    for mod in _running_modules:
        logger.info('Kill the module `' + mod.module_name + '`.')
        mod.kill()
    raise RuntimeError('GTFO')
    # reactor.callFromThread(reactor.stop)
    # sys.exit(1)

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
            logger = logging.getLogger()
            logger.exception(e)
            logger.error('Impossible to connect to the `' + module_name + '` module. (%d / %d)', i + 1, nb_try)
            time.sleep(0.5)
        else:
            return sock.makefile('rw')
    logger.error('Impossible to connect to the `' + module_name + '` module.')
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
    if wl is []:
        raise RuntimeError('Impossible to write to the `' + module_name + '` module.')
        return kill()

    conn = wl[0]
    try:
        conn.write(data + '\n')
        conn.flush()
    except IOError:
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
        return kill()

    try:
        return json.loads(conn.readline())
    except (IOError, ValueError) as e:
        logger = logging.getLogger()
        logger.exception(e)
        logger.error('Impossible to read from the module')
        return kill()
    except TypeError as e:
        logger = logging.getLogger()
        logger.exception(e)
        logger.error('The module send bad data')
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
            return ans.get('success', False)
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
        return super(BaseMeta, cls).__new__(cls, name, parents, attrs)

    def __call__(self, *args, **kwargs):
        obj = super(BaseMeta, self).__call__(*args, **kwargs)
        cls = type(obj)

        # Handle module name
        if not hasattr(obj, 'module_name'):
            if not hasattr(cls, 'module_name'):
                setattr(obj, 'module_name', cls.__name__)
            else:
                setattr(obj, 'module_name', cls.module_name)

        if obj.module_name in type(self).ls_name:
            raise NameError('Module with same name already exist')
        type(self).ls_name.add(obj.module_name)

        # Handle module socket (server side)
        setattr(obj, 'module_socket', path.socket_file(obj.module_name))
        try:
          os.remove(obj.module_socket)
        except OSError:
            pass # TODO logging ?
        endpoint = ServerEndpoint(reactor, obj.module_socket)
        endpoint.listen(connection.Factory(obj))

        # Handle module fields
        ls_fields = []
        for f_cls in cls.__dict__.keys():
            f_cls = getattr(cls, f_cls)
            if isinstance(f_cls, type) and issubclass(f_cls, fields.Base):
                field = f_cls()
                setattr(obj, field.field_name, prop_field(field))
                setattr(field, 'module', obj)
                ls_fields += [field]
        setattr(obj, 'module_fields', ls_fields)

        _running_modules.append(obj)
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

class Base(threading.Thread):
    """
    Base module, subclass this if only core module functionalities are needed.
    """
    __metaclass__ = BaseMeta

    update_rate = 1
    public_name = ''

    def __init__(self, **kwargs):
        super(Base, self).__init__()
        _setup_module(self, **kwargs)
        self.running = False
        self.endpoint = None
        self.update_rate = type(self).update_rate

    def get_info(self):
        """
        Return a dictionnary containing all informations about
        the module.
        """
        ans = {}
        ans['name'] = self.module_name
        ans['public_name'] = type(self).public_name
        ans['update_rate'] = type(self).update_rate
        ans['fields'] = []
        for f in self.module_fields:
            try:
                info = f.get_info()
            except TypeError:
                pass # On ignore le field
            else:
                if info:
                    ans['fields'] += [info]
        return ans

    def start(self):
        logger = logging.getLogger()
        logger.info('The module `' + self.module_name + '` is running.')
        self.running = True
        for f in self.module_fields:
            f.start()
        super(Base, self).start()

    def run(self):
        while self.running:
            time.sleep(0.1)

    def stop(self):
        for f in self.module_fields:
            f.stop()
            f.join(1)
        self.running = False

    def kill(self):
        for f in self.module_fields:
            f.on_kill()
            f.stop()
            try:
                f.join(1)
            except RuntimeError:
                pass
        self.running = False

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

def is_ready(module_name):
    """
    Return if the module *module_name* is ready.
    This is detected by watching the socket file of the module.
    """
    return os.path.exists(path.socket_file(module_name))

def use_module(module_name):
    """
    Shortcut for referencing a module through network, given its module name.
    """
    name = path.realname(module_name)
    if not instance.status(name):
        logger = logging.getLogger()
        logger.info(
                'Try to launch the `' + module_name + '` dependancy module.')

        instance.invoke(name, True)
        t = time.time()
        while not is_ready(module_name):
            time.sleep(0.1)
            if time.time() - t > SOCKET_TIMEOUT:
                logger.error('Impossible to launch the `' + \
                        module_name + '` dependancy module. Abort')
                return kill()
                # raise RuntimeError('Impossible to launch the `' + module_name + '` dependancy module.')

        logger.info('The `' + module_name + \
                '` dependancy module successfully launched.')
    return Network(name=module_name)
