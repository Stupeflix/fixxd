import os
import logging

logger = logging.getLogger(__name__)


class cd(object):

    """
    A context manager that changes the current working directory.
    """

    def __init__(self, path):
        self.path = path
        self.prev_cwd = None

    def __enter__(self):
        self.prev_cwd = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.prev_cwd)
