class Module:
    name = ''
    fields = []

    def __new__(self):
        pass

    def __getattribute__(self, name):
        return None

    def __setattribute__(self, name, value):
        pass
