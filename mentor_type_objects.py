#/usr/bin/python3

"""
Definition of type mentor objects
"""
#
# Author: Alfredo Oltra
# Date: 17/7/2017
#
# License GPL-3.0

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
LIST_ITEM_TYPE = 8
LIST_PARAGRAPH_TYPE = 9
LINK_TYPE = 10
MARKER_TYPE = 11

# styles
STYLE_NAMES = {
    HEADING_TYPE: ['Heading_20_'],
    REMARK_TYPE:  ['MT_20_Observaciones_20_', 'MT_20_Remarks_20_']
    }
