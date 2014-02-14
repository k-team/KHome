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
