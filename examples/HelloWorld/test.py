from buildit.system.unix import Unix

hello = Unix("Hello World")
hello.add('source/')
hello.run()
