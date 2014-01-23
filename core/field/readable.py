class Readable(object):
    def read(self):
        return self.get_value()

    def read_old(self, t):
        return self.get_value(t)
