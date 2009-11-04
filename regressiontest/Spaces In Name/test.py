from buildit.system.unix import Unix

test = Unix('Spaces In Name')
test.add('src/')
test.run()
