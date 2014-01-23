import threading
import fields, fields.io, fields.persistant, time

def read_field(field):
    def _read_field(**kwargs):
        return field.read(**kwargs)
    return _read_field

def write_field(field):
    def _write_field(value):
        return field.write(value)
    return _write_field

class ModuleMeta(type):
    ls_name = set()

    def __new__(cls, name, parents, attrs):
        return super(ModuleMeta, cls).__new__(cls, name, parents, attrs)

    def __call__(self, *args, **kwargs):
        obj = super(ModuleMeta, self).__call__(*args, **kwargs)
        cls = type(obj)

# Gestion du nom du module
        if not hasattr(cls, 'module_name'):
            setattr(obj, 'module_name', cls.__name__)
        else:
            setattr(obj, 'module_name', cls.module_name)

        if obj.module_name in type(self).ls_name:
            raise AttributeError
        type(self).ls_name.add(obj.module_name)

# Gestion des fields du module
        ls_fields = []
        for f_cls in cls.__dict__.keys():
            f_cls = getattr(cls, f_cls)
            if isinstance(f_cls, type) and issubclass(f_cls, fields.Base):
                field = f_cls()
                get_name = 'get_' + field.field_name
                set_name = 'set_' + field.field_name
                if hasattr(obj, get_name) or hasattr(obj, set_name):
                    raise AttributeError
                setattr(obj, get_name, read_field(field))
                setattr(obj, set_name, write_field(field))
                ls_fields += [field]
        setattr(obj, 'module_fields', ls_fields)

        return obj

class Base(threading.Thread):
    __metaclass__ = ModuleMeta

    # module_name = 'Module'

    class Field(fields.io.Readable, fields.io.Writable, fields.persistant.Volatile, fields.Base):
        field_name = 'mon_nom'
        pass

    def __init__(self):
        super(Base, self).__init__()
        self.running = False
        # print self.module_fields
        print self.__dict__
        # module_fields = []

    # def __getattribute__(self, name):
    #     return None

    # def __setattribute__(self, name, value):
    #     pass

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

if __name__ == '__main__':
    b = Base()
    print b.__dict__
    print b.get_mon_nom()
    print b.set_mon_nom(10)
    print b.get_mon_nom()
    print b.get_mon_nom(t=time.time())
    print b.get_mon_nom(fr=time.time() - 5, to=time.time())
    for i in xrange(10):
        b.set_mon_nom(i)
        time.sleep(0.1)

    print b.get_mon_nom(fr=time.time() - 0.5, to=time.time())
