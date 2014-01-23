class Persistant(object):
    def get_value(self):
        raise NotImplementedError

    def get_old_value(self, t):
        raise NotImplementedError

    def set_value(self, t, value):
        raise NotImplementedError

class DBPersistant(Persistant):
    def get_value(self):
        return None

    def get_old_value(self, t):
        return None

    def set_value(self, t, value):
        pass

class VolatilePersistant(Persistant):
    nb_persisted_volatile_values = 100

    def __init__(self):
        super(VolatilePersistant, self).__init__()
        self._persisted_volatile_values = []

    def get_value(self):
        if self._persisted_volatile_values:
            return sorted(self._persisted_volatile_values,
                    key = lambda x: x[0])[-1]
        return super(VolatilePersistant, self).get_value()

    def get_old_value(self, t):
        if self._persisted_volatile_values:
            v = sorted(self._persisted_volatile_values,
                    key = lambda x: abs(x[0] - t))
            if abs(v[0] - t) <= type(self).update_rate:
                return v
        return super(VolatilePersistant, self).get_old_value(t)

    def set_value(self, t, value):
        self._persisted_volatile_values += [(t, value)]
        if len(self._persisted_volatile_values)
            > type(self).nb_persisted_volatile_values:
                self._persisted_volatile_values = \
                        self._persisted_volatile_values[1:]

