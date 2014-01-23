import time

class Writable(object):
    def write(self, value):
        return self._set_value(time.time(), value)

class Readable(object):
    def read(self, **kwargs):
        if 't' in kwargs:
            return self._get_value_at(kwargs['t'])
        if 'fr' in kwargs and 'to' in kwargs:
            return self._get_value_from_to(kwargs['fr'], kwargs['to'])
        return self._get_value()
