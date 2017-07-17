#/usr/bin/python3

"""
General Mentor Objects (MO)
"""
#
# Author: Alfredo Oltra
# Date: 3/5/2017
#
# License GPL-3.0

import os
from mentor_type_objects import *

import element_processor as ep

################
## GENERAL    ##
################

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

        os.makedirs(ep.ElementProcessor.get_directory_target() + "/l1_" + str(self.number))

    def get_string(self):
        """
        Get the string of the block
        """
        return ep.ElementProcessor.get_string_from_tag(self.element)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Number:" + str(Chapter.number) + "\nBlock:" + str(self.element) + \
               "\nSections:\n" + str(self.inner_objects)

class Content(object):
    """
    General content. Parent class of the different types of Content
    """
    def __init__(self, ty, element, parent=None, style=None):
        """
        type: type of content.
        """
        self.type = ty
        self.parent = parent

        if style is None and element != None:
            self.element_style = element.get('text:style-name')
        else:
            self.element_style = style

        self.inner_objects = ep.ElementProcessor.get_inner_mentor_objects(element, self)


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

from mo_inline import *
