import buildit.platform.platform
import buildit.target.target

class Project:
    def __init__(self, name):
        self.name = name
        self.platforms = []
        self.targets = []
        self.require_libraries = []

    def add_platform(self, platform):
        self.platforms.append(platform)
        return platform

    def add_target(self, target):
        self.targets.append(target)
        print "Added new target"
        return target

    def require_lib(self, lib):
        if isinstanceof(lib, (tuple, list)):
            libraries = flatten(lib)
        else:
            libraries = [lib]
        for library in libraries:
            self.required_libraries.append(library)
        return 0

    def run(self):
        for target in self.targets:
            target.start()
        return 0
