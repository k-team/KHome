import time
import fields
import fields.io
import fields.syntax
import module as _module

def basic(new_field, module_name, field_name):
    """
    Return a new class named *new_field* acting like a field proxy of the
    field *field_name* inside the extern module *module_name*.
    This new field is readable and writable. If *field_name* is not, use
    proxy.readable or proxy.writable instead.
    """

    module = _module.use_module(module_name)
    field = getattr(module, field_name)
    field_info = module.fields_info[field_name]

    class Field(
            fields.io.Writable,
            fields.io.Readable,
            fields.Base):
        name = field_info['name']

        def get_info(self):
            # a = super(Field, self).get_info()
            # field_info.update(a)
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

    r_module = _module.use_module(r_module_name)
    w_module = _module.use_module(w_module_name)
    r_field = getattr(r_module, r_field_name)
    w_field = getattr(w_module, w_field_name)
    r_field_info = r_module.fields_info[r_field_name]
    w_field_info = w_module.fields_info[w_field_name]

    if 'type' in r_field_info and 'type' in w_field_info:
        if r_field_info['type'] != w_field_info['type']:
            raise RuntimeError('The two fields have to be of the same type.')

    class Field(
            fields.io.Writable,
            fields.io.Readable,
            fields.Base):
        def get_info(self):
            # a = super(Field, self).get_info()
            # w_field_info.update(a)
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

    module = _module.use_module(module_name)
    field = getattr(module, field_name)
    field_info = module.fields_info[field_name]

    class Field(
            fields.Base):
        def get_info(self):
            # a = super(Field, self).get_info()
            # field_info.update(a)
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

    module = _module.use_module(module_name)
    field = getattr(module, field_name)
    field_info = module.fields_info[field_name]

    class Field(
            fields.io.Writable,
            fields.Base):
        def get_info(self):
            # a = super(Field, self).get_info()
            # field_info.update(a)
            return field_info

        def write(self, value):
            return field(value)

    return type(field_info['name'].encode('ascii', 'ignore'), (Field,), dict())
