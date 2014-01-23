class Type(object):
    def acquire_value(self, value):
        return None

class Numeric(Type):
    def acquire_value(self):
        try:
            return float(super(Type, self).acquire_value(value))
        except ValueError:
            return None

class Boolean(Type):
    def acquire_value(self):
        try:
            return bool(super(Type, self).acquire_value(value))
        except ValueError:
            return None

class String(Type):
    def acquire_value(self):
        try:
            return str(super(Type, self).acquire_value(value))
        except ValueError:
            return None
