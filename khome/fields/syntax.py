from khome.fields import modes, persistant

class Typed(object):
    def get_info(self):
        info = super(Typed, self).get_info()
        info['type'] = type(self).typed_name
        return info

    def set_value(self, t, value):
        if value is None:
            return False
        try:
            value = type(self).typed_type(value)
        except ValueError:
            return False
        return super(Typed, self).set_value(t, value)

class Constant(modes.Readable,
               persistant.Volatile):
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

class Integer(Typed):
    typed_type = int
    typed_name = 'numeric'

class Boolean(Typed):
    typed_type = bool
    typed_name = 'boolean'

class String(Typed):
    @staticmethod
    def typed_type(v):
        return v.encode('utf-8')
    typed_name = 'string'

class BoundNumeric(Numeric):
    """
    Bound numeric field mixin, assumes that *lower_bound* and *upper_bound* are
    set for this field.
    """
    lower_bound = 0
    upper_bound = 0

    def set_value(self, t, value):
        return type(self).lower_bound <= float(value) <= type(self).upper_bound \
                and super(BoundNumeric, self).set_value(t, value)

    def get_info(self):
        info = super(BoundNumeric, self).get_info()
        info['bounded'] = True
        info['value_min'] = type(self).lower_bound
        info['value_max'] = type(self).upper_bound
        return info

class Percentage(BoundNumeric):
    """
    Percentage field, bound numeric field [0;100].
    """
    lower_bound, upper_bound = 0, 100

def from_string(s):
    """
    Return the corresponding syntax class from its string
    representation. Return String class by default.

    TODO construct a dictionary from meta definitions and return from it,
    rather than hard-coding all the types.
    """
    if s == 'numeric':
        return Numeric
    elif s == 'boolean':
        return Boolean
    elif s == 'string':
        return String
    return String

def to_string(cls):
    """
    Return the string representation of a syntax class or a
    syntax class instance. Return 'string' by default.
    """
    return getattr(cls, 'typed_name', 'string')
