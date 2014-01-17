class Type(object):
    def acquire_value(self):
        raise NotImplementedError

class Numeric(Type):
    def acquire_value(self):
        return None

class Boolean(Type):
    def acquire_value(self):
        return None

class String(Type):
    def acquire_value(self):
        return None
