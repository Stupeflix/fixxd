import os
import types

class cd(object):
    """
    A context manager that changes the current working directory.
    """

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.prev_cwd = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.prev_cwd)

def copy_func(f, name=None):
    return types.FunctionType(f.func_code, f.func_globals, name or f.func_name,
        f.func_defaults, f.func_closure)
