"""
Time a snippet of code
======================
"""


import time


class clock(object):
    """
    """
    def __init__(self, name=None):
        """
        """
        self.name = name if name else 'snippet'

    def __enter__(self):
        """
        """
        self.start = time.time()
        return self

    def __exit__(self, *args):
        """
        """
        self.end = time.time()
        self.time = self.end - self.start
