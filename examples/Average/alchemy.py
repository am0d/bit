from buildit import *

average = Project("Average")
with average.add_target(Executable()) as executable:
    executable.add('src')
average.run()
