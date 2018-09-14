"""
Time a snippet of code
======================
"""


import time


class clock(object):
    """
    """
    def __init__(self):
        """
        """
        self.start = None
        self.time = None

    def __enter__(self):
        """
        """
        self.start = time.time()
        return self

    def __exit__(self, *args):
        """
        """
        end = time.time()
        self.time = end - self.start
