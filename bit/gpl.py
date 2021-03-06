# Global Project Lookup

import gc
import sys
import time
import threading

from optparse import OptionParser

from bit.harbinger import Harbinger

# We are Harbinger
class GPL(Harbinger):

    def __init__(self):
        Harbinger.__init__(self)
        if not gc.isenabled():
            gc.enable()
        self.project_dict = { }
        self.project_list = [ ]
        self.parser = OptionParser(conflict_handler='resolve')
        self.parser.add_option('-n', '--no-color', action='store_true',
                               dest='no_color', default=False,
                               help='Text does not use colors')
        self.parser.add_option('-s', '--sequential', action='store_true',
                               dest='sequential', default=False,
                               help='Run projects one at a time')
        self.parser.add_option('-q', '--quiet', action='store_true',
                               dest='quiet', default=False,
                               help='Minimal Information Printed')
        self.parser.add_option('-a', '--hash', action='store', type='string',
                               dest='hash_type', default='md5',
                               help='Which hash algorithm to use.')

    def run(self):
        self.options, self.args = self.parser.parse_args()
        self.parser.destroy() # We don't need the actual parser anymore
        for project in self.project_list:
            if self.options.sequential:
                project.run()
            else:
                project.start()
        while threading.active_count < 1:
            time.sleep(1)

    def project(self, *instances):
        for instance in instances:
            self.project_list.append(instance)
            self.project_dict['{1}|{0}'.format(instance.project_name, instance.name)] = instance

    def path(self, *directories):
        path_list = []
        directories = flatten(list(directories))
        for path in os.environ['PATH'].split(os.pathsep):
            path_list.append(path)
        for directory in directories:
            path_list.append(directory)
        path_list = os.pathsep.join(path_list)
        os.environ['PATH'] = path_list
