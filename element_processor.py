#/usr/bin/python3

"""
Element processor for mentor
Receives xml elements and return mentor objects
"""
#
# Author: Alfredo Oltra
# Date: 3/5/2017
#
# License GPL-3.0

from mentor_type_objects import *
from mo_general import *
from mo_block import *
from mo_inline import *

from Uhuru.data_utilities import Singleton

class ElementProcessor(metaclass=Singleton):
    """
    Manages the process of each xml element (EX) of the document
    Singleton pattern because we need to initialize it
    """
    __elements_with_levels_style_list = {}
    __list_style_list = {}
    __general_style_list = {}
    __previous_mentor_object = None
    __directory_target = ""

    __current_chapter = 0

    __markers = []

    def __init__(self, directory_target=None, style_list=None,
                 list_style_list=None):
        """
        Initializes the ElementProcessor object
        """
        ElementProcessor.__directory_target = directory_target

        # styles which style:parent-style-name is style_X where X is in [1..10]
        # and style is one key of __elements_with_levels_style_list dictionary
        for key in STYLE_NAMES:
            ElementProcessor.__elements_with_levels_style_list[key] = {}
            for level in range(1, 10):
                lst_tmp = []
                for style in STYLE_NAMES[key]:
                    lst_tmp += ElementProcessor.__create_styles_for_level(style, level, style_list)

                ElementProcessor.__elements_with_levels_style_list[key][level] = lst_tmp

        ElementProcessor.__create_list_style_for_level(list_style_list)
        ElementProcessor.__create_general_styles(style_list)
        ElementProcessor.__current_chapter = 0

        return

    @classmethod
    def get_current_chapter(cls):
        return cls.__current_chapter

    @classmethod
    def set_current_chpater(cls, chapter):
        cls.__current_chapter = chapter
        return

    @classmethod
    def add_marker(cls, marker):
        cls.__markers.append(marker)
        return

    @classmethod
    def get_chapter_marker(cls, name):
        for mark in cls.__markers:
            if mark.name == name:
                return mark.chapter

        print("Error 4: Marker chapter (",name,") not found.")
        exit(-4)    

    @classmethod
    def __create_general_styles(cls, style_list):
        """
        Fills the __general_style_list with the different styles
        """
        if style_list is None:
            return

        for style in style_list:
            style_data = {}
   
            paragraph_properties = style.findChild('style:paragraph-properties')
            if paragraph_properties and paragraph_properties.has_attr('fo:margin-left'):
                style_data['margin-left'] = paragraph_properties['fo:margin-left']

            cls.__general_style_list[style.get('style:name')] = style_data

        return

    @classmethod
    def __create_list_style_for_level(cls, list_style_list):
        """
        Fills the __list_style_list with the different list_styles, assign
        the for each level the type of list: number or bullet
        Each entry has a dictionary with the keys: kind, margin-left
        """
        if list_style_list is None:
            return

        for style in list_style_list:
            cls.__list_style_list[style['style:name']] = {}
            level = 0
            for child in style:
                style_data = {}
                level += 1
                if child.name == "text:list-level-style-number":
                    style_data['kind'] = List.TYPE_NUMBER
                else:
                    style_data['kind'] = List.TYPE_BULLET

                child_l3 = child.findChild().findChild()
                style_data['margin-left'] = child_l3['fo:margin-left']

                cls.__list_style_list[style['style:name']][level] = style_data

            # print(style['style:name'], level, cls.__list_style_list[style['style:name']][level])

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

    @staticmethod
    def get_string_from_tag(tag):
        """
        Get the string of the tag (XML element), joining the strings of its children
        """
        string = ""
        for child in tag.children:
            if child.string:
                string += str(child.string)
        return string

    @classmethod
    def is_list_paragraph(cls, element):
        if cls.__previous_mentor_object is None:
            return False

        if isinstance(cls.__previous_mentor_object, Content) == False:
            return False
    
        # TODO que pasa con los remarks y con text_body?? Si se hace bien la gestion se deberia de poder
        # quitar los if internos
        ## previous
        if cls.__previous_mentor_object.type == LIST_TYPE:
            #print("LIST:", cls.__previous_mentor_object.element_style)
            #print("Level1:", cls.__previous_mentor_object.level)
            if cls.__previous_mentor_object.element_style not in cls.__list_style_list:
                return False
            margin_left_previous = cls.__list_style_list[cls.__previous_mentor_object.element_style][cls.__previous_mentor_object.level]
        elif cls.__previous_mentor_object.type == LIST_PARAGRAPH_TYPE:
            if cls.__previous_mentor_object.element_style not in cls.__general_style_list:
                return False
            margin_left_previous = cls.__general_style_list[cls.__previous_mentor_object.element_style]
        else:
            return False

        if 'margin-left' in margin_left_previous:
            margin_left_previous = margin_left_previous['margin-left'][:-2]
        else:
            return False

        ## current
        if element.get('text:style-name') not in cls.__general_style_list:
            return False

        margin_left_current = cls.__general_style_list[element.get('text:style-name')]
        if 'margin-left' in margin_left_current:
            margin_left_current=margin_left_current['margin-left'][:-2]
        else:
            return False
        
        if abs(float(margin_left_previous)-float(margin_left_current)) < 0.05:
            return True
    
        return False

    @classmethod
    def get_directory_target(cls):
        """
        Return the directory target
        """
        return cls.__directory_target

    @classmethod
    def get_type_list(cls, style, lvl):
        """
        Return the type list for a style and a level
        """
        try:
            return cls.__list_style_list[style][lvl]['kind']
        except KeyError: # by default bullet type
            return List.TYPE_BULLET

    @classmethod
    def get_level_number(cls, input_style, style_type=None):
        """
        Return the level of the style
        """
        if style_type is None:
            for key_style in cls.__elements_with_levels_style_list.keys():
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

        for key, value in cls.__elements_with_levels_style_list[style_type].items():
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
            style_l1 = cls.__elements_with_levels_style_list[HEADING_TYPE][1]
            if element_style in style_l1:  # Chapter
                mentor_object = Chapter(element)
            else:
                mentor_object = Heading(element)

        # paragraphs not empty
        elif element.name == 'text:p' and cls.has_string(element):
            # check the type of paragraph
            if Remark.remark_category(element) > 0:
                mentor_object = Remark(element)     ## Remarks
            elif cls.is_list_paragraph(element):
                mentor_object = ListParagraph(element)  ## Inner paragraph list
            else:
                mentor_object = Paragraph(element)  ## Paragraphs

         # lists not empty
        elif element.name == 'text:list' and cls.has_string(element):
            mentor_object = List(element)
        
        elif element.name == 'text:p':
            mentor_object = None
        else:
            mentor_object = NoSupport(element)

        if mentor_object:
            cls.__previous_mentor_object = mentor_object

        return mentor_object

    @classmethod
    def get_inner_mentor_objects(cls, element, parent=None): 
        """
        Return a list of children elements of content.
        element: xml element
        parent: mentor object parent
        return: mentor object list
        """
        mentor_object_list = []
        if element is None:
            return mentor_object_list

        for child in element.children:
            if child.name == 'text:note' and cls.has_string(child):     ## footnotes
                mentor_object_list.append(Footnote(child, parent))
                continue
            if child.name == 'text:p' and cls.has_string(child):       ## paragraphs
                mentor_object_list.append(Paragraph(child, parent))
                continue
            if child.name == 'text:span' and cls.has_string(child):    ## general inline element
                mentor_object_list.append(Span(child, parent))
                continue
            if child.name == 'text:list-item' and cls.has_string(child):    ## list-items
                mentor_object_list.append(List.Item(child, parent))
                continue
            if child.name == 'text:list' and cls.has_string(child):    ## list
                mentor_object_list.append(List(child, parent, parent.parent.level+1))
                continue
            if child.name == 'text:a' and cls.has_string(child):    ## link
                mentor_object_list.append(Link(child, parent))
                continue
            if child.name == 'text:bookmark-start' or child.name == 'text:bookmark':
                mentor_object_list.append(Bookmark(child, parent))
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
    
    @classmethod
    def finalize(cls, chapters):
        """
        Method to finalize the process
        """
        def change_link(io):
            if io.type == LINK_TYPE:
                if io.link[0] == '#':  # internal link
                    chapter = cls.get_chapter_marker(io.link[1:])
                    if io.chapter != chapter:
                        io.link = "../l1_" + str(chapter) + "/Chapter.html" + io.link
            for ioi in io.inner_objects:
                change_link(ioi)
        # update links
        for mo in chapters:
            for io in mo.inner_objects:
                change_link(io)       
                    
        return

