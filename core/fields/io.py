import time

class Writable(object):
    """
    Mixin of the fields.Base class adding a writing property of the value of
    the field. When the value is written, a new timestamp is associated to the
    value and then given to the field's _set_value. It's not garantee that the
    new value is really written.
    Return if the new value is written.
    """

    def get_info(self):
        a = super(Writable, self).get_info()
        a['writable'] = True
        return a

    def write(self, value):
        return self._set_value(time.time(), value)

class Readable(object):
    """
    Mixin of the fields.Base class adding a reading property of the value of
    the field.

    No argument is given : the result correspond to the last saved
    value with its saved time as a tuple (time, value). If there isn't any
    saved values, None is returned

    The argument `t` is given : the result correspond to the value which its saved time is the nearest of `t`.
    """

    def get_info(self):
        a = super(Readable, self).get_info()
        a['readable'] = True
        return a

    def read(self, **kwargs):
        if 't' in kwargs:
            return self._get_value_at(kwargs['t'])
        if 'fr' in kwargs and 'to' in kwargs:
            return self._get_value_from_to(kwargs['fr'], kwargs['to'])
        return self._get_value()

class Graphable(Readable):
    def get_info(self):
        a = super(Graphable, self).get_info()
        a['graphable'] = True
        return a

class Hidden(object):
    def get_info(self):
        return None
