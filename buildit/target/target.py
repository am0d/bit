from threading import Thread

class Target(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        self.build([])

    def build(self, files):
        pass

    def clean(self, files):
        pass

    def add(self, files):
        pass

    def create_link_string(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
