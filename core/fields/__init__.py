import threading
import time

class Base(threading.Thread):
    name = ''
    update_rate = 0

    def __init__(self):
        super(Base, self).__init__()
        self.old_time = 0
        self.update_rate = Base.update_rate
        self.running = False

    def _acquire_value(self):
        '''
        Function called during a data acquisition.
        This method is automatically called at every loop's turns of the
        thread.
        Return None if there is nothing to acquire.
        '''
        return None

    def _set_value(self, t, value):
        '''
        Add a new value *value* at time *t*.
        It's the job of the persistant mixins to manage how to save the new
        value.
        The integrity of the value is done by the type mixins.
        Return True if the add is done. Else False.
        '''
        return True

    def _get_value(self):
        raise NotImplementedError

    def _get_old_value(self, t):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    def read_old(self, t):
        raise NotImplementedError

    def write(self, value):
        raise NotImplementedError

    def _close(self):
        '''
        Method close when the thread is finishing.
        Let the mixins override this to garantee a good shutting of the field.
        '''
        pass

    def start(self):
        '''
        Start the thread of this Field.
        '''
        self.running = True
        super(Base, self).start()

    def stop(self):
        '''
        Ask for a stop of this thread. The thread will stop at the end of the
        loop's turn.
        You may use the join method to be sure the thread is done.
        '''
        self.running = False

    def run(self):
        '''
        Main function of the thread. Every *update_rate* time, try to acquire a value and to
        add this one.
        '''
        while self.running:
            if time.time() - self.old_time >= self.update_rate:
                self.old_time = time.time()
                self._set_value(time.time(), self._acquire_value())
            time.sleep(0.1)
        self._close()
