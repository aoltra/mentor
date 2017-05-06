"""
Helper classes for mentor
"""
#
# Author: Alfredo Oltra
# Date: 3/5/2017
#
# License GPL-3.0

class Chapter(object):
    """
    Chapter class implementation
    """
    def __init__(self, number, block):
        self.number = number
        self.block = block

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Number:" + str(self.number) + "\nBlock:" + str(self.block)
