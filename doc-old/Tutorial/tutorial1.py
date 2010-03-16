# buildit 0.2 - Fly By Night

from buildit import *
project = Unix('buildit_tutorial')
project.add('src')
project.add_include_directory('include')
project.add_library('a', 'b')

# Threaded Version
# project.start()

# Normal Version
project.run()
