import threading
import time

class Field(threading.Thread):
    name = ''
    update_rate = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.old_time = 0
        self.running = False

    def acquire_value(self):
        raise NotImplementedError

    def set_value(self, value):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError

    def get_old_value(self, time):
        raise NotImplementedError

    def start(self):
        self.running = True
        threading.Thread.start(self)

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            if time.time() - self.old_time >= Field.update_rate:
                self.old_time = time.time()
                self.set_value((time.time(), self.acquire_value()))
            time.sleep(0.1)

class Writable(object):
    def set_value(self, value):
        pass

class Readable(object):
    def get_value(self):
        return None

    def get_old_value(self, time):
        return None

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

class Numeric(object):
    def acquire_value(self):
        return None

class Boolean(object):
    def acquire_value(self):
        return None

class String(object):
    def acquire_value(self):
        return None

