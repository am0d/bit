    def clean(self):
        clean_list = [self.object_directory, self.build_directory]
        for item in clean_list:
            if os.path.exists(item) and not item == os.getcwd():
                try:
                    shutil.rmtree(item)
                except OSError:
                    pass
        if os.path.exists('.buildit'):
            try:
                shutil.rmtree('.buildit')
            except OSError:
                pass
        return 0

    def rebuild(self):
        if os.path.exists('.buildit'):
            try:
                shutil.rmtree('.buildit')
            except OSError:
                pass
        return 0
