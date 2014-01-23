import time

class Writable(object):
    def write(self, value):
        self._set_value(time.time(), value)

class Readable(object):
    def read(self):
        return self._get_value()

    def read_old(self, t):
        return self._get_value(t)
