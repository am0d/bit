from threading import Thread
from buildit.utils import flatten

class Target(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self._files = []

    def run(self):
        self.build([])

    def build(self, files):
        pass

    def clean(self, files):
        pass

    def add(self, files):
        self._files.append(files)
        self._files = flatten(self._files)

    def create_link_string(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
