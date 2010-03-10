# I'm Commander Shephard, and this is my favorite module in buildit

class Harbinger(object):
    __shared_state = { }
    def __init__(self):
        self.__dict__ = self.__shared_state
