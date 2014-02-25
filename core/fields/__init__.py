import time
import threading
import logging

# fields export
import io
import syntax
import proxy
import sensor
import actuator
import persistant

class FieldMeta(type):
    def __new__(cls, name, parents, attrs):
        return super(FieldMeta, cls).__new__(cls, name, parents, attrs)

    def __call__(self, *args, **kwargs):
        obj = super(FieldMeta, self).__call__(*args, **kwargs)
        cls = type(obj)

        if not hasattr(cls, 'field_name'):
            setattr(obj, 'field_name', cls.__name__)
        else:
            setattr(obj, 'field_name', cls.field_name)

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

    def get_update_rate(self):
        if self.field_name != 'weather':
            return 1
        try:
            return type(self).update_rate
        except AttributeError:
            return self.module.update_rate

    def get_info(self):
        """
        Return a dictionnary containing all informations about
        the field. Mixins can (and has to) overload this function
        to add more information
        """

        return {'name': self.field_name,
                'update_rate': self.get_update_rate(),
                'public_name': type(self).public_name}

    def on_start(self):
        """
        Function called at the start of the field
        Usefull for init something.
        """
        time.sleep(type(self).sleep_on_start)
        if type(self).init_value is not None:
            self.emit_value(type(self).init_value)

    def emit_value(self, value):
        if value is not None:
            return self.set_value(time.time(), value)
        return False

    def acquire_value(self):
        """
        Function called during a data acquisition.
        This method is automatically called at every loop's turns of the
        thread.
        Return None if there is nothing to acquire.
        """
        return None

    def set_value(self, t, value):
        """
        Add a new value *value* at time *t*.
        It's the job of the persistant mixins to manage how to save the new
        value.
        The integrity of the value is done by the type mixins.
        Return if the add is done.
        """
        return False

    def _get_value(self):
        return None

    def _get_value_at(self, t):
        return None

    def _get_value_from_to(self, fr, to):
        return []

    def close(self):
        """
        Method close when the thread is finishing.
        Let the mixins override this to garantee a good shutting of the field.
        """
        pass

    def always(self):
        """
        Function executed by the field at each loop turn.
        """
        pass

    def read(self, **kwargs):
        return False
        # raise NotImplementedError

    def write(self, value):
        return False
        # raise NotImplementedError

    def start(self):
        """
        Start the thread of this Field.
        """
        self.running = True
        super(Base, self).start()

    def stop(self):
        """
        Ask for a stop of this thread. The thread will stop at the end of the
        loop's turn.
        You may use the join method to be sure the thread is done.
        """
        self.running = False

    def run(self):
        """
        Main function of the thread. Every *update_rate* time, try to acquire a value and to
        add this one.
        """
        self.on_start()
        while self.running:
            if time.time() - self.old_time >= self.get_update_rate():
                self.old_time = time.time()
                self.emit_value(self.acquire_value())
                self.always()
            time.sleep(0.1)
        self.close()

    def on_kill(self):
        """
        Method called when the module is killed. Let the field to
        stop properly.
        """
        pass
