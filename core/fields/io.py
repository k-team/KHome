import time

class Writable(object):
    def write(self, value):
        return self._set_value(time.time(), value)

class Readable(object):
    def read(self):
        return self._get_value()

    def read_at(self, t):
        return self._get_value_at(t)

    def read_from_to(self, fr, to):
        return self._get_value_from_to(fr, to)
