class Persistant(object):
    def get_value(self, time):
        raise NotImplementedError

    def get_old_value(self, time):
        raise NotImplementedError

    def set_value(self, value):
        raise NotImplementedError

class DBPersistant(Persistant):
    def get_value(self, time):
        return None

    def get_old_value(self, time):
        return None

    def set_value(self, value):
        pass

def VolatilePersistant(nb_persisted_values):
    def add_values(instance, value):
        instance.values += [value]
        d = len(instance.values) - nb_persisted_values
        if d > 0:
            instance.values = instance.values[d:]

    class _VolatilePersistant(Persistant):
        def __init__(self):
            self.values = []

        def get_value(self, time):
            return None

        def get_old_value(self, time):
            return None

        def set_value(self, value):
            pass

    return _VolatilePersistant
