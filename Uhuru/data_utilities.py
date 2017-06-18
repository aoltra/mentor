"""
Data Python utilities
"""

class Singleton(type):
    """
    A metaclass that creates a Singleton base class when called.
    A metaclass is the class of a class; that is, a class is an instance of its metaclass.
    Idea from https://stackoverflow.com/a/6798042
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def is_sequence(arg):
    """
    return True if arg is a list or a tuple
    Idea from http://stackoverflow.com/a/1835259
    """
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))
