<<<<<<< HEAD:core/module.py
import time
import threading
import json
import socket
import fields
import fields.io, fields.persistant, fields.sensor, time
=======
import os
import threading
from twisted.internet import reactor
from twisted.internet.endpoints import UNIXServerEndpoint as ServerEndpoint
import core.fields
import connection
>>>>>>> module-communication:core/module/__init__.py

def prop_field(field):
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
        raise Exception
    return _prop_field

def get_module_conn(module_name):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # sock.connect(module_name + '.sock')
    return sock

def get_network_fields(module_conn):
    request = {}
    # module_conn.send(json.dumps(request))
    # data = json.loads(module_conn.recv())
    # parse data
    return ['F2']

<<<<<<< HEAD:core/module.py
def prop_network_field(field):
    def _prop_network_field(*args, **kwargs):
        if len(args) == 1 and not kwargs:
            return False # write
        elif not args:
            if not kwargs:
                return None # read()
            if len(kwargs) == 1 and 't' in kwargs:
                return None # read(t=..)
            if len(kwargs) == 2 and 'fr' in kwargs and 'to' in kwargs:
                return None # read(fr=.., to=..)
        raise Exception
    return _prop_network_field

class BaseMeta(type):
=======
def get_module_socket(module_name):
# TODO rearrange this
    return module_name + '.sock'

class ModuleMeta(type):
>>>>>>> module-communication:core/module/__init__.py
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

<<<<<<< HEAD:core/module.py
        # Handle module fields
=======
# Gestion du socket du module
        setattr(obj, 'module_socket', get_module_socket(obj.module_name))
        try:
          os.remove(obj.module_socket)
        except OSError:
          print 'Petite erreur en voulant supprimer', obj.module_socket
          pass
        endpoint = ServerEndpoint(reactor, obj.module_socket)
        endpoint.listen(connection.Factory(obj))

# Gestion des fields du module
>>>>>>> module-communication:core/module/__init__.py
        ls_fields = []
        for f_cls in cls.__dict__.keys():
            f_cls = getattr(cls, f_cls)
            if isinstance(f_cls, type) and issubclass(f_cls, core.fields.Base):
                field = f_cls()
                setattr(obj, field.field_name, prop_field(field))
                ls_fields += [field]
        setattr(obj, 'module_fields', ls_fields)

        return obj

class Base(threading.Thread):
    __metaclass__ = BaseMeta

    def __init__(self, **kwargs):
        super(Base, self).__init__()
        self.running = False
        self.endpoint = None

        if 'name' in kwargs:
            self.module_name = kwargs['name']
        #module_fields = []

    def start(self):
        self.running = True
        for f in self.module_fields:
            f.start()
        super(Base, self).start()

    def run(self):
        while self.running:
            pass

    def stop(self):
        for f in self.module_fields:
            f.stop()
            f.join(1)
        self.running = False

class NetworkMeta(type):
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
        conn = get_module_conn(obj.module_name)
        setattr(obj, 'module_conn', conn)

# Gestion des fields du module
        ls_field = get_network_fields(obj.module_conn)
        for field in ls_field:
            setattr(obj, field, prop_network_field(field))

        return obj

class Network(object):
    __metaclass__ = NetworkMeta

    def __init__(self, **kwargs):
        super(Network, self).__init__()

        if 'name' in kwargs:
            self.module_name = kwargs['name']

def use_module(module_name):
    return Network(name=module_name)

if __name__ == '__main__':
    M2 = use_module('M2')

    class M1(Base):
        class Field(fields.io.Readable,
                fields.io.Writable,
                fields.persistant.Volatile,
                fields.Base):
            field_name = 'mon_nom'

            def acquire_value(self):
                return M2.F2()
                return (int(time.time()) % 10) ** 2

        class F1(fields.io.Readable,
                fields.io.Writable,
                fields.persistant.Volatile,
                fields.sensor.Sensor,
                fields.Base):
            pass

    a = M1(name='M0')
    b = M1()
    print b.mon_nom()
    print b.mon_nom(10)
    print b.mon_nom()
    print b.mon_nom(t=time.time())
    print b.mon_nom(fr=time.time() - 5, to=time.time())
    for i in xrange(10):
        b.mon_nom(i)
        # time.sleep(0.1)

    print b.mon_nom(fr=time.time() - 0.5, to=time.time())
    print b.mon_nom()
    print b.mon_nom(fr=time.time() - 0.5, to=time.time())

    print b.F1(10)
    print b.F1()

    print a.mon_nom(fr=0, to=time.time())

<<<<<<< HEAD:core/module.py
    # b.start()
    # try:
    #     while True:
    #         print b.mon_nom()
    #         time.sleep(0.4)
    # except KeyboardInterrupt:
    #     b.stop()
    #     b.join(1)

    class M2(Network):
        pass

    M2 = use_module('M2')
    print M2.module_name
    print M2.__dict__
    print M2.F2()
=======
    reactor.run()

    b.start()
    try:
        while True:
            print b.mon_nom()
            time.sleep(0.4)
    except KeyboardInterrupt:
        b.stop()
        b.join(1)
>>>>>>> module-communication:core/module/__init__.py
