import fields.io
import fields.persistant

class Typed(object):
    def get_info(self):
        info = super(Typed, self).get_info()
        info['type'] = type(self).typed_name
        return info

    def _set_value(self, t, value):
        if value is None:
            return False
        try:
            value = type(self).typed_type(value)
        except ValueError:
            return False
        return super(Typed, self)._set_value(t, value)

class Constant(fields.io.Readable, fields.persistant.Volatile):
    update_rate = 100000
    const_value = None

    def get_info(self):
        info = super(Constant, self).get_info()
        info['const'] = True
        return info

    def acquire_value(self):
        return type(self).const_value

class Numeric(Typed):
    typed_type = float
    typed_name = 'numeric'

class Boolean(Typed):
    typed_type = bool
    typed_name = 'boolean'

class String(Typed):
    typed_type = str
    typed_name = 'string'

class BoundNumeric(Numeric):
    """
    Bound numeric field mixin, assumes that *lower_bound* and *upper_bound* are
    set for this field.
    """
    def _set_value(self, t, value):
        return super(BoundNumeric, self)._set_value(t, value) \
                and type(self).lower_bound < value < type(self).upper_bound

class Percentage(BoundNumeric):
    """
    Percentage field, bound numeric field [0;100].
    """
    lower_bound, upper_bound = 0, 100

def from_string(s):
    """
    Return the corresponding syntax class from its string
    representation.
    Return String class when the representation is ill-formed.
    """
    if s == 'numeric':
        return Numeric
    elif s == 'boolean':
        return Boolean
    elif s == 'string':
        return String
    return String

def to_string(s):
    """
    Return the string representation of a syntax class or a
    syntax class instance.
    Return 'string' class when there is no match is ill-formed.
    """
    if s == Numeric or isinstance(s, Numeric):
        return 'numeric'
    elif s == Boolean or isinstance(s, Boolean):
        return 'boolean'
    elif s == String or isinstance(s, String):
        return 'string'
    return 'string'
