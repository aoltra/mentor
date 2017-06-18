#/usr/bin/python3

"""
Helper classes for mentor
"""
#
# Author: Alfredo Oltra
# Date: 3/5/2017
#
# License GPL-3.0

from mentor import get_string_from_tag
from Uhuru.data_utilities import Singleton

# global variables
# type elements
NOSUPPORTED_TYPE = -1
HEADING_TYPE = 0
PARAGRAPH_TYPE = 1
REMARK_TYPE = 2
FOOTNOTE_TYPE = 3
TEXT_TYPE = 4

# styles
STYLE_NAMES = {
    HEADING_TYPE: ['Heading_20_'],
    REMARK_TYPE:  ['MT_20_Observaciones_20_', 'MT_20_Remarks_20_']
    }

class ElementProcessor(metaclass=Singleton):
    """
    Manages the process of each element of the document
    Singleton pattern
    """
    __style_list = {}

    def __init__(self, style_list):
        """
        Initializes the ElementProcessor object
        """
        # styles which style:parent-style-name is style_X where X is in [1..10]
        # and style is and key of __Style_list dictionary
        for key in STYLE_NAMES:
            for style in STYLE_NAMES[key]:
                for level in range(1, 10):
                    self.__style_list[style + str(level)] =\
                            self.__create_styles_for_level(style, level, style_list)

        return

    @classmethod
    def __create_styles_for_level(cls, style_element, level_number, style_list):
        """
        Creates a list of styles for element and level
        style_element: style of element to search
        level_number: level of style
        style_list: source of styles
        """
        style_name = style_element + str(level_number)

        styles = list((style['style:name'] for style in style_list
                       if style.get('style:parent-style-name') == style_name))

        styles.append(style_name)

        return styles

    def process_element(self, element):
        """
        Processes a first level xml element
        """
        mentor_object = None
        # headings not empty
        if element.name == "text:h" and self.has_string(element):
            print("")
        # paragraphs not empty
        elif element.name == 'text:p' and self.has_string(element):
            if Remark.remark_category(element) > 0:
                mentor_object = Remark(element)     ## Remarks
            else:
                mentor_object = Paragraph(element)  ## Paragraphs
        else:
            mentor_object = NoSupport(element)

        return mentor_object

    @classmethod
    def has_string(cls, tag):
        """
        Return true if the tag has a string
        """
        for child in tag.children:
            if child.string:
                return True

        return False

    def get_inner_elements(self, element):
        """
        Return a list of children elements of content.
        """
        elements_list = []
        if element is None:
            return elements_list

        for child in element.children:
            if child.name == 'text:note' and self.has_string(child):     ## footnotes
                elements_list.append(Footnote(child))
                continue
            if child.name == 'text:p' and self.has_string(child):       ## paragraphs
                elements_list.append(Paragraph(child))
                continue

            if child.string: ## if is not any of the previous types
                elements_list.append(Text(child.string))
                continue

        return elements_list


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
    """
    General content. Parent class of the different types of Content
    """
    elements = []
    def __init__(self, ty, element):
        """
        type: type of content.
        """
        processor = ElementProcessor(None)
        self.type = ty
        self.elements = processor.get_inner_elements(element)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Type:" + str(self.type)


####################
## BLOCK ELEMENTS ##
####################

class Heading(Content):
    "Internal heading model"
    def __init__(self, level, string):
        """
        level: heading level
        string: text body of the paragraph
        """
        self.level = level
        self.string = string
        Content.__init__(self, 0, None)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return super(Heading, self).__repr__() + \
            " Level:" + str(self.level) + "\nBlock:" + str(self.string)


class Paragraph(Content):
    "Paragraph model"
    def __init__(self, element):
        """
        element: xml element
        """
        self.element = element
        Content.__init__(self, PARAGRAPH_TYPE, element)
        print("ELEMENT:", self.elements)

        return

    def is_style(self, style_type):
        "Return true if the paragraph style is one of the style_type"
        paragraph_style = self.element.get('text:style-name')
        for key in STYLE_NAMES:
            if key == style_type:
                for style in STYLE_NAMES[key]:
                    if paragraph_style.startswith(style):
                        return True
        return False


class Remark(Content):
    "Remark element model"
    category = 0
    elements = []

    def __init__(self, element, category=0):
        """
        element: xml element
        category: type of remarks 1..3
        """
        Content.__init__(self, REMARK_TYPE, element)

        if category != 0:
            self.category = self.remark_category(element)

#        self.paragraphs = []
#        for paragraph in paragraphs:
#            self.paragraphs.append(Paragraph(paragraph.string))

        return

    @staticmethod
    def remark_category(paragraph):
        """
        Return the category of the Remark if the paragraph is a Remark (number greater than 0).
        Otherwise return 0
        """
        category = 0
        paragraph_style = paragraph.get('text:style-name')
        if paragraph.is_style(REMARK_TYPE):
            category = int(paragraph_style[paragraph_style.rfind('_')+1:])

        return category



#####################
## INLINE ELEMENTS ##
#####################
# pylint: disable=too-few-public-methods
class Text(Content):
    "Simple text model"
    string = ""

    def __init__(self, string):
        """
        string: body text
        """
        Content.__init__(self, TEXT_TYPE, None)
        self.string = string

        return


class Footnote(Content):
    "Footnote model"
    citation = ""

    def __init__(self, element):
        Content.__init__(self, FOOTNOTE_TYPE, element)
        self.__get_note_components(element)

        return

    def __get_note_components(self, element):
        """
        Get the elements values for Footnote
        """
        for child in element.children:
            if child.name == 'text:note-citation':
                self.citation = child.string
            if child.name == 'text:note-body':
                self.citation = child.string

# pylint: disable=too-few-public-methods
class NoSupport(Content):
    "Elements no supported"
    def __init__(self, element):
        Content.__init__(self, NOSUPPORTED_TYPE, None)
        return

    def __str__(self):
        return "NOT SUPPORTED"
