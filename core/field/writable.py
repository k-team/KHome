import time

class Writable(object):
    def write(self, value):
        self.set_value(time.time(), value)
