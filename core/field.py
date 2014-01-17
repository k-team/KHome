class Field(object):
    name = ''
    category = 'int'
    writable = False
    default_value = 0

    def __init__(self):
        value = Field.default_value

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return None

class Writable(object):
    def write(self, value):
        pass

class Readable(object):
    def read(self):
        return None

class DBPersistant(object):
    db_persist_rate = 0

    def set_value(self, value):
        pass

    def get_value(self, time):
        return None

class VolatilePersistant(object):
    volatile_persist_rate = 0

    def set_value(self, value):
        pass

    def get_value(self, time):
        return None
