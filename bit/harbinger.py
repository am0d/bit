# I'm Commander Shephard, and this is my favorite module in bit

class Harbinger(object):
    __shared_state = { }
    def __init__(self):
        self.__dict__ = self.__shared_state
