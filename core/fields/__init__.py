import threading
import time

class Base(threading.Thread):
    name = ''
    update_rate = 0

    def __init__(self):
        super(Base, self).__init__(self)
        self.old_time = 0
        self.running = False

    def acquire_value(self):
        return None

    def set_value(self, t, value):
        pass

    def get_value(self):
        raise NotImplementedError

    def get_old_value(self, t):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    def read_old(self, t):
        raise NotImplementedError

    def write(self, value):
        raise NotImplementedError

    def start(self):
        self.running = True
        super(Base, self).start(self)

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            if time.time() - self.old_time >= type(self).update_rate:
                self.old_time = time.time()
                self.set_value(time.time(), self.acquire_value())
            time.sleep(0.1)
