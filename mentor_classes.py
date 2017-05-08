"""
Helper classes for mentor
"""
#
# Author: Alfredo Oltra
# Date: 3/5/2017
#
# License GPL-3.0

class Block(object):
    """
    Block class implementation
    """
    def __init__(self, number, block):
        self.number = number
        self.block = block
        self.sections = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Number:" + str(self.number) + "\nBlock:" + str(self.block) + \
               "\nSections:\n" + str(self.sections)

class Section(object):
    """
    Section class implementation. Children block elements
    """
    def __init__(self, level, block):
        """
        level: heading level
        """
        self.level = level
        self.block = block

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Level:" + str(self.level) + "\nBlock:" + str(self.block)
