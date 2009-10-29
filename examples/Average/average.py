from buildit.system.system import System as System
from buildit.compiler.cc import CC as CC
from buildit.linker.ld import LD as LD

average = System("Average")

average.compiler = CC()
average.compiler.object_dir = 'object'
average.add_files(['src/main.c', 'src/get_numbers.c',
                    'src/average.c'])

average.linker = LD()
average.linker.target = 'average'
average.run()
