#/usr/bin/python3

"""
Helper classes for mentor
"""
#
# Author: Alfredo Oltra
# Date: 3/5/2017
#
# License GPL-3.0

import os

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
FOOTNOTE_BODY_TYPE = 5
SPAN_TYPE = 6
LIST_TYPE = 7

# styles
STYLE_NAMES = {
    HEADING_TYPE: ['Heading_20_'],
    REMARK_TYPE:  ['MT_20_Observaciones_20_', 'MT_20_Remarks_20_']
    }

class ElementProcessor(metaclass=Singleton):
    """
    Manages the process of each xml element (EX) of the document
    Singleton pattern because we need to initialize it
    """
    __style_list = {}
    __list_style_list = {}
    __directory_target = ""

    def __init__(self, directory_target=None, style_list=None,
                 list_style_list=None):
        """
        Initializes the ElementProcessor object
        """
        ElementProcessor.__directory_target = directory_target

        # styles which style:parent-style-name is style_X where X is in [1..10]
        # and style is one key of __style_list dictionary
        for key in STYLE_NAMES:
            ElementProcessor.__style_list[key] = {}
            #for level in range(1, 10):
             #   ElementProcessor.__style_list[key].setdefault(level, [])
            for level in range(1, 10):
                lst_tmp = []
                for style in STYLE_NAMES[key]:
                    lst_tmp += ElementProcessor.__create_styles_for_level(style, level, style_list)

                ElementProcessor.__style_list[key][level] = lst_tmp

        ElementProcessor.__create_list_style_for_level(list_style_list)

        return

    @classmethod
    def __create_list_style_for_level(cls, list_style_list):
        """
        Fills the __list_style_list with the different list_styles, assign
        the for each level the type of list: number or bullet
        """
        if list_style_list is None:
            return

        for style in list_style_list:
            cls.__list_style_list[style['style:name']] = {}
            level = 0
            for child in style:
                level += 1
                if child.name == "text:list-level-style-number":
                    cls.__list_style_list[style['style:name']][level] = List.TYPE_NUMBER
                else:
                    cls.__list_style_list[style['style:name']][level] = List.TYPE_BULLET
        return

    @staticmethod
    def __create_styles_for_level(style_element, level_number, style_list):
        """
        Creates a list of styles for xml element and level.
        It is a static method because doesn't need the object (self)
        style_element: style of xml element to search
        level_number: level of style
        style_list: source of styles
        """
        style_name = style_element + str(level_number)

        styles = list((style['style:name'] for style in style_list
                       if style.get('style:parent-style-name') == style_name))

        styles.append(style_name)
        return styles

    @classmethod
    def has_string(cls, tag):
        """
        Return true if the tag has a string. It works in recursive way
        It is a static method because don't needs the object (self)
        """
        for child in tag.children:
            if child.string:
                return True
            elif cls.has_string(child) is True:
                return True

        return False

    @classmethod
    def get_directory_target(cls):
        """
        Return the directory target
        """
        return cls.__directory_target

    @classmethod
    def get_level_number(cls, input_style, style_type=None):
        """
        Return the level of the style
        """
        if style_type is None:
            for key_style in cls.__style_list.keys():
                level_number = cls.__chek_style_in_style_list(key_style, input_style)
                if level_number != -1:
                    break
        else:
            level_number = cls.__chek_style_in_style_list(style_type, input_style)

        if level_number == -1:
            print("Error 3: Style not found.")
            exit(-3)

        return level_number

    @classmethod
    def __chek_style_in_style_list(cls, style_type, input_style):
        """
        style_type: style type to search
        Return -1 if teh style does not exist
        """
        level_number = -1

        for key, value in cls.__style_list[style_type].items():
            if input_style in value:
                level_number = key
                break

        return level_number

    @classmethod
    def process_element(cls, element):
        """
        Processes a xml element
        element: xml element to process
        return: mentor object
        """
        mentor_object = None
        element_style = element.get('text:style-name')

        # headings not empty
        if element.name == "text:h" and cls.has_string(element):
            style_l1 = cls.__style_list[HEADING_TYPE][1]
            if element_style in style_l1:  # Chapter
                mentor_object = Chapter(element)
            else:
                mentor_object = Heading(element)

        # paragraphs not empty
        elif element.name == 'text:p' and cls.has_string(element):
            # check the type of paragraph
            if Remark.remark_category(element) > 0:
                mentor_object = Remark(element)     ## Remarks
            else:
                mentor_object = Paragraph(element)  ## Paragraphs

         # lists not empty
      #  elif element.name == 'text:list' and cls.has_string(element):
       #     pass
        else:
            mentor_object = NoSupport(element)

        return mentor_object

    @classmethod
    def get_inner_mentor_objects(cls, element):
        """
        Return a list of children elements of content.
        element: xml element
        return: mentor object list
        """
        mentor_object_list = []
        if element is None:
            return mentor_object_list

        for child in element.children:
            if child.name == 'text:note' and cls.has_string(child):     ## footnotes
                mentor_object_list.append(Footnote(child))
                continue
            if child.name == 'text:p' and cls.has_string(child):       ## paragraphs
                mentor_object_list.append(Paragraph(child))
                continue
            if child.name == 'text:span' and cls.has_string(child):    ## general inline element
                mentor_object_list.append(Span(child))
                continue

            if child.string: ## if is not any of the previous types
                mentor_object_list.append(Text(child.string))
                continue

        return mentor_object_list

    #pylint: disable-msg=C0103
    @classmethod
    def get_inner_mentor_objects_by_type(cls, mentor_object, object_type):
        """
        Return a list of mentor_object, children of a mentor_object and the
        whose type is object_type
        mentor_object: mentor object root
        object_type: type object to compare
        return: list of mentor objects children of mentor_object whose type is object_type
        """
        mentor_object_list = []
        if mentor_object is None:
            return mentor_object_list

        for child_obj in mentor_object.inner_objects:
            if isinstance(child_obj, object_type):
                mentor_object_list.append(child_obj)

            inner_objects = cls.get_inner_mentor_objects_by_type(child_obj, object_type)
            mentor_object_list.extend([obj for obj in inner_objects if obj != []])

        return mentor_object_list


class Chapter(object):
    """
    Chapter class implementation
    """
    number = 0

    def __init__(self, element):
        Chapter.number += 1
        self.number = Chapter.number
        self.element = element
        self.inner_objects = []

        os.makedirs(ElementProcessor.get_directory_target() + "/l1_" + str(self.number))

    def get_string(self):
        """
        Get the string of the block
        """
        return get_string_from_tag(self.element)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Number:" + str(Chapter.number) + "\nBlock:" + str(self.element) + \
               "\nSections:\n" + str(self.inner_objects)

class Content(object):
    """
    General content. Parent class of the different types of Content
    """
    def __init__(self, ty, element):
        """
        type: type of content.
        """
        self.type = ty
        self.inner_objects = ElementProcessor.get_inner_mentor_objects(element)

        if element != None:
            self.element_style = element.get('text:style-name')
        else:
            self.element_style = None

    def get_raw_text(self):
        """
        Return the raw text of the content
        """
        return Content.__get_inner_text(self)

    @staticmethod
    def is_style(element, style_type):
        """
        Returns true if the element style is one of the style_type
        element: element to study
        style_type: style type, ie, HEADING_TYPE, PARAGRAPH_TYPE...
        """
        style_element = element.get('text:style-name')
        for style in STYLE_NAMES[style_type]:
            if style_element.startswith(style):
                # if style ends with space the style_element have to end with a nunber
                if style.endswith('_20_') and style == style_element:
                    return False

                return True

        return False

    @classmethod
    def __get_inner_text(cls, mentor_object):
        """
        Private function
        Return a string with the text of all inner objects of a mentor_objects
        mentor_object: mentor object
        """
        string = ""
        for obj in mentor_object.inner_objects:
            if isinstance(obj, Text):
                string += str(obj.string)
            else:
                string += cls.__get_inner_text(obj)

        return string

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Type:" + str(self.type)


####################
## BLOCK ELEMENTS ##
####################

class Heading(Content):
    """
    Internal heading model
    """
    def __init__(self, element):
        """
        level: heading level
        string: text body of the paragraph
        """
        Content.__init__(self, HEADING_TYPE, element)
        self.level = ElementProcessor.get_level_number(self.element_style)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return super(Heading, self).__repr__() + \
            " Level:" + str(self.level) + "\nBlock:" + str(self.get_raw_text())


class Paragraph(Content):
    """
    Paragraph model
    """
    def __init__(self, element):
        """
        element: xml element
        """
        self.element = element
        Content.__init__(self, PARAGRAPH_TYPE, element)

        return

class List(Content):
    """
    List model
    """
    TYPE_BULLET = 1
    TYPE_NUMBER = 2

    def __init__(self, element):
        Content.__init__(self, LIST_TYPE, element)
        return

class Remark(Content):
    """
    Remark element model
    """
    def __init__(self, element, category=0):
        """
        element: xml element
        category: type of remarks 1..3
        """
        self.category = category

        Content.__init__(self, REMARK_TYPE, element)

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



#####################
## INLINE ELEMENTS ##
#####################

# pylint: disable=too-few-public-methods
class Text(Content):
    """
    Simple text model
    """
    def __init__(self, string):
        """
        string: body text
        """
        Content.__init__(self, TEXT_TYPE, None)
        self.string = string

        return


class Span(Content):
    """
    Span element model
    """
    def __init__(self, element):
        """
        element: span xml element
        """
        Content.__init__(self, SPAN_TYPE, element)
        return


class Footnote(Content):
    """
    Footnote model
    """
    class Body(Content):
        """
        Body content of footnote
        """
        def __init__(self, element):
            Content.__init__(self, FOOTNOTE_BODY_TYPE, element)
            return

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
                self.body = Footnote.Body(child)

# pylint: disable=too-few-public-methods
class NoSupport(Content):
    """
    Elements no supported
    """
    def __init__(self, element):
        Content.__init__(self, NOSUPPORTED_TYPE, None)
        return

    def __str__(self):
        return "NOT SUPPORTED"
