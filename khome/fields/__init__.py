import time
import threading
import logging

import actuator
import modes
import persistant
import proxy
import sensor
import syntax

__all__ = ('actuator', 'modes', 'persistant',
           'proxy', 'sensor', 'syntax',
           'Base', 'make')

class FieldMeta(type):
    """
    Metaclass for field building, mainly for defining the field's name.
    """
    def __call__(self, *args, **kwargs):
        obj = super(FieldMeta, self).__call__(*args, **kwargs)
        cls = type(obj)

        # set the field's name from either the field_name or the class' name
        setattr(obj, 'field_name', getattr(cls, 'field_name', cls.__name__))
        return obj

class Base(threading.Thread):
    __metaclass__ = FieldMeta

    public_name = ''
    sleep_on_start = 0
    init_value = None

    def __init__(self):
        super(Base, self).__init__()
        self.old_time = 0
        self.running = False

    def start(self):
        """
        Start this field's thread.
        """
        self.running = True
        return super(Base, self).start()

    def stop(self):
        """
        Ask for this thread to stop, it will be stopped effectively at the end
        of the current loop. You can use join() method to make sure the thread
        is finished.
        """
        self.running = False

    def run(self):
        """
        Main function of the thread. Every *update_rate* time, try to acquire a value and to
        add this one.
        """
        self._initialize()
        self.on_start()
        while self.running:
            if time.time() - self.old_time >= self.get_update_rate():
                self.old_time = time.time()
                self.emit_value(self.acquire_value())
                self.on_update()
            time.sleep(0.1) # magic number detected
        self.on_close()

    def _initialize(self):
        time.sleep(type(self).sleep_on_start)
        if type(self).init_value is not None and \
                self._get_value() is None:
            self.emit_value(type(self).init_value)

    def _get_value(self):
        return None

    def _get_value_at(self, t):
        return None

    def _get_value_from_to(self, fr, to):
        return []

    def update(self):
        """
        FIXME what is this used for ?
        """
        self.old_time = 0

    def get_update_rate(self):
        """
        Return the effective update rate for this module.
        """
        try:
            return type(self).update_rate
        except AttributeError:
            return self.module.update_rate

    def get_info(self):
        """
        Return a dictionnary containing all informations about
        the field. Mixins can (and have to) overload this function
        to add more information
        """
        return { 'name':        self.field_name,
                 'update_rate': self.get_update_rate(),
                 'public_name': type(self).public_name, }

    def emit_value(self, value):
        """
        Set the field's value programmatically, for example inside a
        custom field.
        """
        if value is not None:
            return self.set_value(time.time(), value)
        return False

    def acquire_value(self):
        """
        Method called during a data acquisition.
        This method is automatically called at each loop run for this thread.
        None is returned if there isn't anything to acquire.
        """
        pass

    def set_value(self, t, value):
        """
        Add a new value *value* at time *t*. It's the job of the persistant
        mixins to manage how to save the new value. The integrity of the value
        is done by the type mixins. Return if the add is done.
        TODO write this is *good* english
        """
        return False

    def on_start(self):
        """
        Event method called when the field's thread is started, can be used for
        initializing.
        """
        pass

    def on_close(self):
        """
        Event method called when the field's thread is finished, can be used
        for teardown operations.
        """
        pass

    def on_update(self):
        """
        Event method called on each loop run, can be used for regular update
        logic.
        """
        pass

    # alias for the on_update event method
    always = on_update

    def read(self, **kwargs):
        return False

    def write(self, value):
        return False

    def on_kill(self):
        """
        Method called when the module is killed. Let the field to
        stop properly.
        """
        pass

_syntax = syntax
def make(name, syntax='string', mode='', persistence='volatile', attrs={}):
    """
    Make a basic field, given its name, type, mode and persistence. Mode can be
    readable (r), writable (w) or a combination of both, whatever the order.
    Valid field types (syntaxes) are documented in fields.syntax. Field
    persistence is any class name defined in fields.persistant.
    Extra attributes (specific to fields) can be given in the *attrs*
    parameter. These are copied in the generated field's __dict__.

    TODO remove field "name" parameter.
    """
    classes = []
    classes.append(_syntax.from_string(syntax.lower()))
    if 'r' in mode:
        classes.append(modes.Readable)
    if 'w' in mode:
        classes.append(modes.Writable)
    classes.append(persistant.Database              \
            if persistence.lower() == 'database'    \
            else persistant.Volatile)
    return type(name, tuple(classes + [Base]), attrs)
