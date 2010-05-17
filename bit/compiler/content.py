import os
import shutil
import filecmp
import subprocess

from bit.compiler.compiler import Compiler
from bit.utils import flatten, file_hash

class Content(Compiler):

    def __init__(self, project_name='PROJECT'):
        Compiler.__init__(self, project_name)

    def __str__(self):
        return 'Content Copier'

    def compile_files(self):
        return 0

    @property
    def extensions(self):
        return ['.*']
