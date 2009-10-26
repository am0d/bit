from buildit.system.system import System as System
from buildit.compiler.cc import CC as CC

average = System("Average")
average.compiler = CC()
average.compiler.object_dir = 'object'
average.add_files(['src/main.c', 'src/get_numbers.c',
                    'src/average.c'])
average.run()
