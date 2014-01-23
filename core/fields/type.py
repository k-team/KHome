class Numeric(object):
    def acquire_value(self):
        try:
            return float(super(Type, self).acquire_value(value))
        except ValueError:
            return None

class Boolean(object):
    def acquire_value(self):
        try:
            return bool(super(Type, self).acquire_value(value))
        except ValueError:
            return None

class String(object):
    def acquire_value(self):
        try:
            return str(super(Type, self).acquire_value(value))
        except ValueError:
            return None
