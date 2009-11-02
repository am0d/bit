from buildit.system.unix import Unix

average = Unix("Average")

average.add_files('src')
average.run()
