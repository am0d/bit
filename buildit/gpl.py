# Global Project Lookup - Not to be confused with GNU Public License ;D
# Enables our garbage collection as well, rather than System

import gc

class GPL(object):

    def __init__(self):
        if not gc.isenabled():
            gc.enable()
        self.__project_lookup = {}
        self.__project_list = []

    def run_t(self):
        pass

    def run(self):
        pass

    def add_project(self, name, instance):
        pass
