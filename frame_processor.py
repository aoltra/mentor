#/usr/bin/python3

"""
Definition of utilities to process frames
"""
#
# Author: Alfredo Oltra
# Date: 11/8/2017
#
# License GPL-3.0

from mo_block import Image
from mo_inline import NoSupport

class FrameProcessor(object):
    """
    Manages the process of each xml element of a frame element
    """
    @staticmethod
    def process_frame(frame):
        """
        Processes a frame element
        frame: xml frame to process
        return: mentor object
        """
        mentor_object = None
        frame_object = Frame(frame)

        if frame is None:
            return mentor_object

        for child in frame.children:
            if child.name == 'draw:image':  # images inside frame
                mentor_object = Image(child, frame_object)
                continue
            else:
                mentor_object = NoSupport(child)

        return mentor_object

class Frame(object):
    """
    Frame model
    """
    def __init__(self, element):
        """
        element: xml element
        """
        self.element = element

        if 'svg:width' in element:
            self.width = element['svg:width']
        else:
            self.width = None

        if 'svg:height' in element:
            self.height = element['svg:height']
        else:
            self.height = None

        return
