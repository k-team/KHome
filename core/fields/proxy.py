import fields
import fields.io
import fields.syntax
from module import use_module

def basic(new_field, module_name, field_name):
    """
    Return a new class named *new_field* acting like a field proxy of the
    field *field_name* inside the extern module *module_name*.
    This new field is readable and writable. If *field_name* is not, use
    proxy.readable or proxy.writable instead.
    """

    module = use_module(module_name)
    field = getattr(module, field_name)
    field_info = module.fields_info[field_name]

    cls_syntax = fields.syntax.String
    if 'type' in field_info:
        cls_syntax = fields.syntax.from_string(field_info['type'])

    class Field(
            fields.io.Writable,
            fields.io.Readable,
            cls_syntax,
            fields.Base):
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

    r_module = use_module(r_module_name)
    w_module = use_module(w_module_name)
    r_field = getattr(r_module, r_field_name)
    w_field = getattr(w_module, w_field_name)
    r_field_info = r_module.fields_info[r_field_name]
    w_field_info = w_module.fields_info[w_field_name]

    cls_syntax = fields.syntax.String
    if 'type' in r_field_info and 'type' in w_field_info:
        if r_field_info['type'] != w_field_info['type']:
            raise RuntimeError('The two fields have to be of the same type.')
        cls_syntax = fields.syntax.from_string(r_field_info['type'])

    class Field(
            fields.io.Writable,
            fields.io.Readable,
            cls_syntax,
            fields.Base):
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

    module = use_module(module_name)
    field = getattr(module, field_name)
    field_info = module.fields_info[field_name]

    cls_syntax = fields.syntax.String
    if 'type' in field_info:
        cls_syntax = fields.syntax.from_string(field_info['type'])

    class Field(
            fields.io.Readable,
            cls_syntax,
            fields.Base):
        def read(self, **kwargs):
            return field(**kwargs)

    return type(new_field, Field.__bases__, dict(Field.__dict__))


def writable(new_field, module_name, field_name):
    """
    Return a new class named *new_field* acting like a field proxy of the
    field *field_name* inside the extern module *module_name*.
    This new field is only writable.
    """

    module = use_module(module_name)
    field = getattr(module, field_name)
    field_info = module.fields_info[field_name]

    cls_syntax = fields.syntax.String
    if 'type' in field_info:
        cls_syntax = fields.syntax.from_string(field_info['type'])

    class Field(
            fields.io.Writable,
            cls_syntax,
            fields.Base):
        def write(self, value):
            return field(value)

    return type(new_field, Field.__bases__, dict(Field.__dict__))
