import fields.io
import fields.persistant

class Constant(fields.io.Readable,
        fields.persistant.Volatile):
    update_rate = 100000
    const_value = None

    def get_info(self):
        a = super(Constant, self).get_info()
        a['const'] = True
        return a

    def acquire_value(self):
        return type(self).const_value

class Numeric(object):
    def get_info(self):
        a = super(Numeric, self).get_info()
        a['type'] = 'numeric'
        return a

    def _set_value(self, t, value):
        if value is None:
            return False
        try:
            value = float(value)
        except ValueError:
            return False
        return super(Numeric, self)._set_value(t, value)

class Boolean(object):
    def get_info(self):
        a = super(Boolean, self).get_info()
        a['type'] = 'boolean'
        return a

    def _set_value(self, t, value):
        if value is None:
            return False
        try:
            value = bool(value)
        except ValueError:
            return False
        return super(Boolean, self)._set_value(t, value)

class String(object):
    def get_info(self):
        a = super(String, self).get_info()
        a['type'] = 'string'
        return a

    def _set_value(self, t, value):
        if value is None:
            return False
        try:
            value = str(value)
        except ValueError:
            return False
        return super(String, self)._set_value(t, value)

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
