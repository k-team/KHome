import os
import threading
import json
import socket
import time
from twisted.internet import reactor
from twisted.internet.endpoints import UNIXServerEndpoint as ServerEndpoint

import fields
from . import connection

_file = os.path.realpath(__file__)
_root = os.path.dirname(os.path.dirname(os.path.dirname(_file)))

MODULES_DIRECTORY = os.path.join(_root, 'modules')
INSTANCES_DIRECTORY = os.path.join(_root, 'instances')

def get_module_directory(module_name):
    """
    Shortcut to get the directory for a module (absolute path).
    """
    return os.path.join(MODULES_DIRECTORY, module_name)

def get_instance_directory(module_name):
    """
    Shortcut to get the directory for a instance of a module (absolute path).
    """
    return INSTANCES_DIRECTORY

def get_socket_name(module_name):
    """
    Return the filename of the socket of the module named *module_name*.
    TODO add instance system.
    """
    return os.path.join(get_instance_directory(module_name), module_name + '.sock')

def get_socket(module_name):
    """
    Return a socket connected to the module named *module_name*.
    The socket is transformed by the makefile function and has to be use as a
    file object.
    """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(get_socket_name(module_name))
    return sock.makefile('rw')

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
    module_conn.write(json.dumps(request) + '\n')
    module_conn.flush()
    ans = json.loads(module_conn.readline())
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
            request['field_value'] = field_value
            module_conn.write(json.dumps(request))
            ans = json.loads(module_conn.readline())
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

            module_conn.write(json.dumps(request) + '\n')
            module_conn.flush()
            ans = json.loads(module_conn.readline())

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
        setattr(obj, 'module_socket', get_socket_name(obj.module_name))
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
                ls_fields += [field]
        setattr(field, 'module', obj)
        setattr(obj, 'module_fields', ls_fields)

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
        for field in fields:
            setattr(obj, field['name'], prop_network_field(conn, field))

        return obj

class Base(threading.Thread):
    """
    Base module, subclass this if only core module functionalities are needed.
    """
    __metaclass__ = BaseMeta

    def __init__(self, **kwargs):
        super(Base, self).__init__()
        _setup_module(self, **kwargs)
        self.running = False
        self.endpoint = None

    def start(self):
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
    return Network(name=module_name)
