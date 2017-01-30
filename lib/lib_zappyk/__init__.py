# -*- coding: utf-8 -*-
__author__ = 'zappyk'

class _initializeVariable:
    def __init__(self, value=None):
        """Construct a initialize variable."""
        if value is not None:
            self.value = value
    def set(self, value):
        """Set the variable to VALUE."""
        self.value = value
        return
    def get(self):
        """Return value of variable."""
        value = self.value
        return(value)