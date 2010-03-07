# Global Project Lookup - Not to be confused with GNU Public License ;D
# Enables our garbage collection as well, rather than System
# Need to possibly look into changing everything to multiprocessing 
# because of the GIL

import gc
import sys
import threading

from buildit.harbinger import Harbinger

from buildit.cprint import error

# We are Harbinger
class GPL(Harbinger):

    def __init__(self):
        Borg.__init__(self)
        if not gc.isenabled():
            gc.enable()
        self.__project_lookup = {}
        self.__project_list = []

    def start(self, no_wait=False):
        for project in self.__project_list:
            project.start()
        if not no_wait:
            while threading.active_count() > 1:
                time.sleep(1)
    
    def run(self):
        for project in self.__project_list:
            project.run()

    def add_project(self, instance):
        self.__project_list.append(instance)
        self.__project_lookup[instance._project_name] = instance

    def remove_project(self, instance):
        try:
            self.__project_list.remove(instance)
        except ValueError:
            pass
        try:
            del self.__project_lookup[instance._project_name]
        except KeyError:
            error('Could not remove: {0}'.format(instance._project_name))

    def pause(self):
        raw_input('Press Enter to continue...')
