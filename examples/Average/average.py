from buildit.system.unix import Unix

average = Unix("Average")

average.add('src')
average.run()
