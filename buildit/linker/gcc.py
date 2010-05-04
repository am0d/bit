# GCC Linker

from buildit.linker.linker import Linker
from buildit.cprint import command
class GCCLinker(Linker):

    def __init__(self, project_name):
        Linker.__init__(self)
        self.executable = 'gcc'

    def run(self, file_list):
        self.file_list = file_list
        run_list = [self.executable, '-o', '"{0}"'.format(self.project_name)] + self.file_list + self.linker_flags
        command('[LINK] {0}'.format(self.project_name))
        try:
            subprocess.call(run_list)
        except OSError:
            os.system(' '.join(run_list))
        return 0
