import os
import sys
import threading

class System(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.build_steps = []
        
        self.build_steps.append(pre_build)
        self.build_steps.append(pre_build)
        self.build_steps.append(pre_build)


    def run(self):
        for function in self.build_steps:
            return_value = function()
            if not return_value == 0:
                error('\nError: {0}'.format(lookup_error(return_value)))

    def pre_build(self):
        pass

    def build(self):
        pass

    def post_build(self):
        pass
