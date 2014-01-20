import threading

class Module(threading.Thread):
    name = ''
    fields = []

    def __new__(self):
        pass

    def __init__(self):
        self.fields = [f() for f in Module.fields]
        self.running = False
        threading.Thread.__init__(self)

    def __getattribute__(self, name):
        return None

    def __setattribute__(self, name, value):
        pass

    def start(self):
        self.running = True
        for f in self.fields:
            f.start()
        threading.Thread.start(self)

    def run(self):
        while self.running:
            pass

    def stop(self):
        for f in self.fields:
            f.stop()
            f.join(1)
        self.running = False
