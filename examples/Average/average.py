from buildit import Unix

average = Unix("Average")
average.add_include_directory('inc')
average.add('src')
average.run()
