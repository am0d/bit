# Global Project Lookup - Not to be confused with GNU Public License ;D
# Enables our garbage collection as well, rather than System

import gc
import threading

class GPL(object):

    def __init__(self):
        if not gc.isenabled():
            gc.enable()
        self.__project_lookup = {}
        self.__project_list = []

    def run_t(self):
        for project_in self.__project_list:
            project.start()
        # We should allow people to disable this part.
        while threading.active_count() > 1:
            time.sleep(1)
    def run(self):
        for project in self.__project_list:
            project.run()

    def add_project(self, instance):
        self.__project_list.append(instance)
        self.__project_lookup[instance._project_name] = instance
