import time
import khome.module
from khome.fields import mode

def _get_mod_info(module_name, field_name):
    """
    Return the information for the field *field_name* for the module
    *module_name*.
    """
    mod = khome.module.use_module(module_name)
    field = getattr(mod, field_name)
    return mod.fields_info[field_name]

def basic(new_field, module_name, field_name):
    """
    Return a new class named *new_field* acting like a field proxy of the
    field *field_name* inside the extern module *module_name*.
    This new field is readable and writable. If *field_name* is not, use
    proxy.readable or proxy.writable instead.
    """
    field_info = _get_mod_info(module_name, field_name)

    from khome.fields import Base as Field
    class Field(mode.Writable, mode.Readable, Field):
        name = field_info['name']

        def get_info(self):
            #a = super(Field, self).get_info()
            #field_info.update(a)
            return field_info

        def read(self, **kwargs):
            if 'fr' in kwargs and 'to' in kwargs:
                return field(fr=-(time.time()-kwargs['fr']), to=-(time.time()-kwargs['to']))
            if 't' in kwargs:
                return field(t=-(time.time()-kwargs['t']))
            return field(**kwargs)

        def write(self, value):
            return field(value)

    return type(field_info['name'].encode('ascii', 'ignore'), (Field,), dict())


def mix(new_field, r_module_name, r_field_name, w_module_name, w_field_name):
    """
    Return a new class named *new_field* acting like a field proxy and
    mixing two fields. This new field is readable and writable. The
    readable part is given by redirecting request to the field
    *r_field_name* of the module *r_module_name*. The writable part is
    given by redirecting request to the field *w_field_name* of the
    module *w_module_name*.
    """
    r_field_info = _get_mod_info(r_module_name, r_field_name)
    w_field_info = _get_mod_info(w_module_name, w_field_name)

    if 'type' in r_field_info and 'type' in w_field_info:
        if r_field_info['type'] != w_field_info['type']:
            raise RuntimeError('The two fields have to be of the same type.')

    from khome.fields import Base as Field
    class Field(mode.Writable, mode.Readable, Field):
        def get_info(self):
            #a = super(Field, self).get_info()
            #w_field_info.update(a)
            return w_field_info

        def read(self, **kwargs):
            if 'fr' in kwargs and 'to' in kwargs:
                return field(fr=-(time.time()-kwargs['fr']), to=-(time.time()-kwargs['to']))
            if 't' in kwargs:
                return field(t=-(time.time()-kwargs['t']))
            return r_field(**kwargs)

        def write(self, value):
            return w_field(value)

    return type(field_info['name'].encode('ascii', 'ignore'), (Field,), dict())


def readable(new_field, module_name, field_name):
    """
    Return a new class named *new_field* acting like a field proxy of the
    field *field_name* inside the extern module *module_name*.
    This new field is only readable.
    """
    field_info = _get_mod_info(module_name, field_name)

    from khome.fields import Base as Field
    class Field(Field):
        def get_info(self):
            #a = super(Field, self).get_info()
            #field_info.update(a)
            return field_info

        def read(self, **kwargs):
            if 'fr' in kwargs and 'to' in kwargs:
                return field(fr=-(time.time()-kwargs['fr']), to=-(time.time()-kwargs['to']))
            if 't' in kwargs:
                return field(t=-(time.time()-kwargs['t']))
            return field(**kwargs)

    return type(field_info['name'].encode('ascii', 'ignore'), (Field,), dict())


def writable(new_field, module_name, field_name):
    """
    Return a new class named *new_field* acting like a field proxy of the
    field *field_name* inside the extern module *module_name*.
    This new field is only writable.
    """
    field_info = _get_mod_info(module_name, field_name)

    from khome.fields import Base as Field
    class Field(mode.Writable, Field):
        def get_info(self):
            #a = super(Field, self).get_info()
            #field_info.update(a)
            return field_info

        def write(self, value):
            return field(value)

    return type(field_info['name'].encode('ascii', 'ignore'), (Field,), dict())
