# Global Project Lookup - Not to be confused with GNU Public License ;D
# Enables our garbage collection as well

import gc
import sys
import multiprocessing

from optparse import OptionParser

from buildit.harbinger import Harbinger
from buildit.cprint import error

# We are Harbinger
class GPL(Harbinger):

    def __init__(self):
        Harbinger.__init__(self)
        if not gc.isenabled():
            gc.enable()
        self.__project_lookup = {}
        self.__project_list = []
        self.parser = OptionParser(conflict_handler='resolve')

        # Global Options
        self.parser.add_option('-n', '--no-color', action='store_true',
                               dest='no_color', 
                               help='Print text without colors.')
        self.parser.add_option('-s', '--sequential', action='store_true',
                               dest='sequential'
                               help='Run through projects one at a time') 

    def run(self):
        self.options, self.args = self.parser.parse_args()
        self.parser.destroy() # No longer needed
        for project in self.__project_list:
            if self.options.sequential:
                project.run()
            else:
                project.start()

    def add_project(self, instance):
        self.__project_list.append(instance)
        self.__project_lookup[instance.project_name] = instance

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
