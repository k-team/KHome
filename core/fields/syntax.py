class Numeric(object):
    def set_value(self, t, value):
        if value is None:
            return False
        try:
            value = float(value)
        except ValueError:
            return False
        return super(Numeric, self).set_value(t, value)

class Boolean(object):
    def set_value(self, t, value):
        if value is None:
            return False
        try:
            value = bool(value)
        except ValueError:
            return False
        return super(Boolean, self).set_value(t, value)

class String(object):
    def set_value(self, t, value):
        if value is None:
            return False
        try:
            value = str(value)
        except ValueError:
            return False
        return super(String, self).set_value(t, value)
