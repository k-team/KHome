class Database(object):
    def _get_value(self):
        return None

    def _get_value_at(self, t):
        return None

    def _get_value_from_to(self, fr, to):
        return []

    def set_value(self, t, value):
        return False

class Volatile(object):
    volpersist_nb_values = 200
    volpersist_save_lost = True

    def __init__(self):
        super(Volatile, self).__init__()
        self._persisted_volatile_values = []

    def _get_value(self):
        if self._persisted_volatile_values:
            return sorted(self._persisted_volatile_values,
                    key = lambda x: x[0])[-1]
        return super(Volatile, self)._get_value()

    def _get_value_at(self, t):
        if self._persisted_volatile_values:
            v = sorted(self._persisted_volatile_values,
                    key = lambda x: abs(x[0] - t))[0]
            if abs(v[0] - t) <= type(self).update_rate:
                return v
        return super(Volatile, self)._get_value_at(t)

    def _get_value_from_to(self, fr, to):
        res = filter(lambda x: fr <= x[0] <= to,
                self._persisted_volatile_values)
        if res:
            return res
        return super(Volatile, self)._get_value_from_to(fr, to)

    def set_value(self, t, value):
        self._persisted_volatile_values += [(t, value)]
        if len(self._persisted_volatile_values) \
            > type(self).volpersist_nb_values:
                if type(self).volpersist_save_lost:
                    lost_value = self._persisted_volatile_values[0]
                    super(Volatile, self).set_value(*lost_value)
                self._persisted_volatile_values = \
                        self._persisted_volatile_values[1:]
        return True
