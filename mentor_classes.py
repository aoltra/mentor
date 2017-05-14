"""
Helper classes for mentor
"""
#
# Author: Alfredo Oltra
# Date: 3/5/2017
#
# License GPL-3.0

from mentor import get_string_from_tag

class Block(object):
    """
    Block class implementation
    """
    def __init__(self, number, block):
        self.number = number
        self.block = block
        self.content = []

    def get_string(self):
        """
        Get the string of the heading block
        """
        print(self.block)
        return get_string_from_tag(self.block)

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
            0: Heading
            1: Paragraph
        """
        self.type = ty

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Type:" + str(self.type)


class Heading(Content):
    "Modeling a internal heading"
    def __init__(self, level, string):
        """
        level: heading level
        string: text body of the paragraph
        """
        self.level = level
        self.string = string
        Content.__init__(self, 0)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return super(Heading, self).__repr__() + \
            " Level:" + str(self.level) + "\nBlock:" + str(self.string)


class Paragraph(Content):
    "Modeling a paragraph"
    def __init__(self, string):
        """
        string: text body of the paragraph
        """
        self.string = string
        Content.__init__(self, 1)


class Remarks(Content):
    "Modeling remarks paragraph"
    def __init__(self, typ, string):
        """
        type: type of remarks 1..3
        """
        self.type = typ
        self.string = string
        Content.__init__(self, 2)
