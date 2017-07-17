#/usr/bin/python3

"""
Menotr Objects type block
"""
#
# Author: Alfredo Oltra
# Date: 3/5/2017
#
# License GPL-3.0

from mentor_type_objects import *
from mo_general import Content

import element_processor as ep

####################
## BLOCK ELEMENTS ##
####################

class Heading(Content):
    """
    Internal heading model
    """
    def __init__(self, element, parent=None):
        """
        level: heading level
        string: text body of the paragraph
        """
        Content.__init__(self, HEADING_TYPE, element, parent)
        self.level = ep.ElementProcessor.get_level_number(self.element_style)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return super().__repr__() + \
            " Level:" + str(self.level) + "\nBlock:" + str(self.get_raw_text())


class Paragraph(Content):
    """
    Paragraph model
    """
    def __init__(self, element, parent=None):
        """
        element: xml element
        """
        self.element = element
        Content.__init__(self, PARAGRAPH_TYPE, element, parent)

        return

class ListParagraph(Content):
    """
    Inner paragraph to lists model
    """
    def __init__(self, element, parent=None):
        """
        element: xml element
        """
        self.element = element
        Content.__init__(self, LIST_PARAGRAPH_TYPE, element, parent)

        return

class List(Content):
    """
    List model
    """
    TYPE_NOT_ASSIGNED = 0
    TYPE_BULLET = 1
    TYPE_NUMBER = 2

    class Item(Content):
        """
        List Item model
        """
        def __init__(self, element, parent):
            Content.__init__(self, LIST_ITEM_TYPE, element, parent, parent.element_style)
            return

        def __str__(self):
            return self.__repr__()

        def __repr__(self):
            return "List.Item -> " + super().__repr__() + "\n" +\
                   "              Parent:" + str(self.parent)

    def __init__(self, element, parent=None, level=1):
        self.level = level
        self.kind = List.TYPE_NOT_ASSIGNED
        if parent is None:
            style = None
        else:
            style = parent.element_style
        Content.__init__(self, LIST_TYPE, element, parent, style)
        self.kind = ep.ElementProcessor.get_type_list(self.element_style, self.level)

        # sublist
        if len(self.inner_objects) == 1:
            if len(self.inner_objects[0].inner_objects) == 1 and \
               self.inner_objects[0].inner_objects[0].type == LIST_TYPE:
                self.inner_objects.append(self.inner_objects[0].inner_objects[0])
                del self.inner_objects[0]
        return

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "List -> " + super().__repr__() + "\n" +\
               "         Level:" + str(self.level) + "\n" +\
               "         Kind: " + str(self.kind)

class Remark(Content):
    """
    Remark element model
    """
    def __init__(self, element, parent=None, category=0):
        """
        element: xml element
        category: type of remarks 1..3
        """
        self.category = category

        Content.__init__(self, REMARK_TYPE, element, parent)

        if category != 0:
            self.category = self.remark_category(element)

#        self.paragraphs = []
#        for paragraph in paragraphs:
#            self.paragraphs.append(Paragraph(paragraph.string))

        return

    @staticmethod
    def remark_category(element):
        """
        Return the category of the Remark if the paragraph is a Remark (number greater than 0).
        Otherwise return 0
        """
        category = 0
        element_style = element.get('text:style-name')
        if Content.is_style(element, REMARK_TYPE):
            category = int(element_style[element_style.rfind('_')+1:])

        return category
