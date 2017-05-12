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
        self.content = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Number:" + str(self.number) + "\nBlock:" + str(self.block) + \
               "\nSections:\n" + str(self.content)

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


class Content(object):
    "Modeling a general content. Parent class of the different types of Content"
    def __init__(self, ty):
        """
        type: type of content.
            0: Header
            1: Paragraph
        """
        self.type = ty

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Type:" + str(self.type)


class Header(Content):
    "Modeling a internal header"
    def __init__(self, level, string):
        """
        level: heading level
        """
        self.level = level
        self.string = string
        Content.__init__(self, 0)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return super(Header, self).__repr__() + \
            " Level:" + str(self.level) + "\nBlock:" + str(self.string)


class Paragraph(Content):
    "Modeling a paragraph"
    def __init__(self):
        """
        """
        Content.__init__(self, 1)
