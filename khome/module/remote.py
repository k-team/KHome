import os
import path
import logging

SOCKET_TIMEOUT = 3

def connect(module_name, nb_try=5):
    """
    Return a socket connected to the module named *module_name*.
    Try this *nb_try* times. If it's unsuccessful, raise a
    RuntimeError.
    The socket is transformed by the makefile function and has to
    be use as a file object.
    """
    for i in xrange(nb_try):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(path.socket_file(module_name))
        except socket.error as e:
            logging.exception(e)
            logging.error('Cannot connect to `%s` module. (%d / %d)',
                    module_name, i + 1, nb_try)
            time.sleep(0.5)
        else:
            return sock.makefile('rw')
    raise RuntimeError('Cannot connect to `%s` module.' % module_name)

def write(conn, data):
    """
    Write *data* to the *conn* file, add a new line character at
    the end and flush the buffer output.
    Wait a maximum *SOCKET_TIMEOUT* sec for writing. If there is a
    timeout, an IOError is raised.
    """
    _, wl, _ = select.select([], [conn], [], SOCKET_TIMEOUT)
    if not wl:
        raise IOError('Cannot write to module.')
    conn = wl[0]
    conn.write(data + '\n')
    conn.flush()

def readline(conn):
    """
    Read a entire line from the *conn* file and transform it into a dict with json.
    Wait a maximum of *SOCKET_TIMEOUT* sec for reading. If there
    is a timeout, a IOError is raised.
    """
    rl, _, _ = select.select([conn], [], [], SOCKET_TIMEOUT)
    if rl is []:
        raise IOError('Cannot read from module.')
    return json.loads(conn.readline())

def get_identification(module_conn):
    """
    Return the list of the fields of a module connected through the
    *module_conn* file socket.
    """
    request = {}
    request['code'] = 'knockknock'
    write(module_conn, json.dumps(request))
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

def is_ready(module_name):
    """
    Return if the module *module_name* is ready.
    This is detected by watching the ready file of the module.
    """
    return os.path.exists(path.ready_file(module_name))

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

class Network(object):
    """
    Network module base, built just like Base module, but with network
    interfacing.
    """
    __metaclass__ = NetworkMeta

    def __init__(self, name):
        super(Network, self).__init__()
        self.module_name = name

def use(module_name):
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
                raise IOError('Cannot launch the `%s` dependency:
                        abort' % module_name)
        logging.info('`%s` dependancy module successfully launched.',
                module_name)
    return Network(name=module_name)
