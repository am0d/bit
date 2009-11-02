from buildit.system.system import System

linux = System("Hello World")
linux.add_files('source')
linux.run()
