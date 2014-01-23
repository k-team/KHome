class Numeric(object):
    def _set_value(self, t, value):
        if value is None:
            return False
        try:
            value = float(value)
        except ValueError:
            return False
        return super(Numeric, self)._set_value(t, value)

class Boolean(object):
    def _set_value(self, t, value):
        if value is None:
            return False
        try:
            value = bool(value)
        except ValueError:
            return False
        return super(Boolean, self)._set_value(t, value)

class String(object):
    def _set_value(self, t, value):
        if value is None:
            return False
        try:
            value = str(value)
        except ValueError:
            return False
        return super(String, self)._set_value(t, value)
