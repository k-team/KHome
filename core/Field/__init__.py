import threading
import time

class Base(threading.Thread):
    name = ''
    update_rate = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.old_time = 0
        self.running = False

    def acquire_value(self):
        raise NotImplementedError

    def set_value(self, value):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError

    def get_old_value(self, time):
        raise NotImplementedError

    def start(self):
        self.running = True
        threading.Thread.start(self)

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            if time.time() - self.old_time >= Field.update_rate:
                self.old_time = time.time()
                self.set_value((time.time(), self.acquire_value()))
            time.sleep(0.1)
