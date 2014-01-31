import core.fields
import core.fields.io
from core.module import use_module

def __init__(new_field, module_name, field_name):
    """
    Return a new class named *new_field* acting like a field proxy of the
    field *field_name* inside the extern module *module_name*.
    This new field is readable and writable. If *field_name* is not, use
    proxy.readable or proxy.writable instead.
    """
    class Field(
            core.fields.io.Writable,
            core.fields.io.Readable,
            core.fields.Base):
        module = use_module(module_name)
        field = getattr(module, field_name)

        def read(self, **kwargs):
            return field(**kwargs)

        def write(self, value):
            return field(value)

    return type(new_field, Field.__bases__, dict(Field.__dict__))

def mix(new_field, r_module_name, r_field_name, w_module_name, w_field_name):
    """
    Return a new class named *new_field* acting like a field proxy and
    mixing two fields. This new field is readable and writable. The
    readable part is given by redirecting request to the field
    *r_field_name* of the module *r_module_name*. The writable part is
    given by redirecting request to the field *w_field_name* of the
    module *w_module_name*.
    """
    class Field(
            core.fields.io.Writable,
            core.fields.io.Readable,
            core.fields.Base):
        r_module = use_module(r_module_name)
        w_module = use_module(w_module_name)
        r_field = getattr(r_module, r_field_name)
        w_field = getattr(w_module, w_field_name)

        def read(self, **kwargs):
            return r_field(**kwargs)

        def write(self, value):
            return w_field(value)

    return type(new_field, Field.__bases__, dict(Field.__dict__))

def readable(new_field, module_name, field_name):
    """
    Return a new class named *new_field* acting like a field proxy of the
    field *field_name* inside the extern module *module_name*.
    This new field is only readable.
    """
    class Field(
            core.fields.io.Readable,
            core.fields.Base):
        module = use_module(module_name)
        field = getattr(module, field_name)

        def read(self, **kwargs):
            return field(**kwargs)

    return type(new_field, Field.__bases__, dict(Field.__dict__))

def writable(new_field, module_name, field_name):
    """
    Return a new class named *new_field* acting like a field proxy of the
    field *field_name* inside the extern module *module_name*.
    This new field is only writable.
    """
    class Field(
            core.fields.io.Writable,
            core.fields.Base):
        module = use_module(module_name)
        field = getattr(module, field_name)

        def write(self, value):
            return field(value)

    return type(new_field, Field.__bases__, dict(Field.__dict__))
