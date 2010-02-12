# Global Project Lookup - Not to be confused with GNU Public License ;D
# Enables our garbage collection as well, rather than System

import gc

class GPL(object):

    def __init__(self):
        if not gc.isenabled():
            gc.enable()
        project_lookup = {}
