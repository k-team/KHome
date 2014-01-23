import time

class Writable(object):
    def write(self, value):
        self.set_value(time.time(), value)

class Readable(object):
    def read(self):
        return self.get_value()

    def read_old(self, t):
        return self.get_value(t)
