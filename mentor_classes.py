"""
Helper classes for mentor
"""
#
# Author: Alfredo Oltra
# Date: 3/5/2017
#
# License GPL-3.0

from mentor import get_string_from_tag

# global variables
# type elements
HEADING_TYPE = 0
PARAGRAPH_TYPE = 1
REMARK_TYPE = 2
FOOTNOTE_TYPE = 3
TEXT_TYPE = 4

# styles
REMARKS_STYLE_NAME_ES = 'MT_20_Observaciones_20_'
REMARKS_STYLE_NAME_EN = 'MT_20_Remarks_20_'

class ElementProcessor(object):
    """
    Manages the process of each element of the document
    """

    @staticmethod
    def process_element(element):
        """
        Processes a first level xml element
        """
        mentor_object = None
        if element.name == 'text:p' and ElementProcessor.has_string(element):
            if Remark.remark_category(element) > 0:
                mentor_object = Remark(element)     ## Remarks
            else:
                mentor_object = Paragraph(element)  ## Paragraphs

        return mentor_object

    @staticmethod
    def has_string(tag):
        """
        Return true if the tag has a string
        """
        for child in tag.children:
            if child.string:
                return True
        return False

    @staticmethod
    def get_inner_elements(element):
        """
        Return a list of children elements of content.
        """
        elements_list = []
        if element is None:
            return elements_list

        for child in element.children:
            if child.name == 'text:note' and ElementProcessor.has_string(child):     ## footnotes
                elements_list.append(Footnote(child))
                continue
            if child.name == 'text:p' and ElementProcessor.has_string(child):       ## paragraphs
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
        self.type = ty
        self.elements = ElementProcessor.get_inner_elements(element)

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
        Content.__init__(self, PARAGRAPH_TYPE, element)
        print("ELEMENT:", self.elements)

        return


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
        Return the category of the Remark if the paragraph is a Remark (number greater than 1).
        Otherwise return 0
        """
        category = 0
        paragraph_style = paragraph.get('text:style-name')
        if paragraph_style.startswith(REMARKS_STYLE_NAME_ES) or\
           paragraph_style.startswith(REMARKS_STYLE_NAME_EN):
            category = int(paragraph_style[paragraph_style.rfind('_')+1:])

        return category



#####################
## INLINE ELEMENTS ##
#####################

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

