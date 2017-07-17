#/usr/bin/python3

"""
Mentor Objects type inline
"""
#
# Author: Alfredo Oltra
# Date: 3/5/2017
#
# License GPL-3.0

from mentor_type_objects import *
from mo_general import *
import element_processor as ep

#####################
## INLINE ELEMENTS ##
#####################

# pylint: disable=too-few-public-methods
class Text(Content):
    """
    Simple text model
    """
    def __init__(self, string, parent=None):
        """
        string: body text
        parent: parent object
        """
        Content.__init__(self, TEXT_TYPE, None, parent)
        self.string = string

        return

class Link(Content):
    """
    URL reference
    """
    def __init__(self, element, parent=None):
        """
        parent: parent object
        """
        Content.__init__(self, LINK_TYPE, element, parent)
        self.chapter = ep.ElementProcessor.get_current_chapter()
        self.link = element['xlink:href']
        
        return

class Bookmark(Content):
    """
    Bookmark model
    """
    def __init__(self, element, parent=None):
        """
        parent: parent object
        """
        Content.__init__(self, MARKER_TYPE, element, parent)
        self.chapter = ep.ElementProcessor.get_current_chapter()
        self.name = element['text:name']
        
        ep.ElementProcessor.add_marker(self)
        return

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Bookmark -> " + super().__repr__() + "\n" +\
               "              Parent:" + str(self.parent) + "\n" +\
               "              name: " + self.name + "\n" +\
               "              chapter: " + str(self.chapter)

class Span(Content):
    """
    Span element model
    """
    def __init__(self, element, parent=None):
        """
        element: span xml element
        """
        Content.__init__(self, SPAN_TYPE, element, parent)
        return

class Footnote(Content):
    """
    Footnote model
    """
    class Body(Content):
        """
        Body content of footnote
        """
        def __init__(self, element, parent=None):
            Content.__init__(self, FOOTNOTE_BODY_TYPE, element, parent)
            return

    def __init__(self, element, parent=None):
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
    def __init__(self, element, parent=None):
        Content.__init__(self, NOSUPPORTED_TYPE, None, parent)
        return

    def __str__(self):
        return "NOT SUPPORTED"
