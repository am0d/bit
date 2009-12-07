import sys
from buildit import Unix

average = Unix("Average")
if sys.platform=='win32':
    from buildit import MSVC
    average.compiler = MSVC()
average.add_include_directory('inc')
average.add('src')
average.run()
