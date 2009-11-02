from buildit.system.unix import Unix

hello = Unix("Hello World")
hello.add_files('source/')
hello.run()
