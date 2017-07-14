"""
odt to html conversor to use in Moodle
"""
#
# Author: Alfredo Oltra
# Date: 3/5/2017
#
# License GPL-3.0

import os
import zipfile
import shutil

from bs4 import BeautifulSoup
from genshi.template import TemplateLoader
import plac

import Uhuru.os_utilities as UH_OSU
import Uhuru.cli_utilities as UH_CLIU
import mentor_classes as mentor

# global variables
REMARKS_STYLE_NAME_ES = 'MT_20_Observaciones_20_'
REMARKS_STYLE_NAME_EN = 'MT_20_Remarks_20_'

def unzip_odt(odt_file):
    """
    unzip the odt file
    """
    directory_to_extract = os.path.splitext(odt_file)[0]
    directory_to_extract += ".mentor.tmp"
    zip_ref = zipfile.ZipFile(odt_file, 'r')
    zip_ref.extractall(directory_to_extract)
    zip_ref.close()
    return directory_to_extract


def create_styles_for_level(style_element, level_number, style_list):
    """
    Create a list of heading styles
    """
    style_name = style_element + str(level_number)

    styles = list((style['style:name'] for style in style_list
                   if style.get('style:parent-style-name') == style_name))

    styles.append(style_name)

    return styles

def get_level_number(level_style, styles):
    """
    Return the heading level of the style
    """
    level_number = list([key for key, value in styles.items() if level_style in value])
    if not level_number:
        print("Error 3: Style not found.")
        exit(-3)

    return int(level_number[0])

def get_string_from_tag(tag):
    """
    Get the string of the tag, joining the strings of its children
    """
    string = ""
    for child in tag.children:
        if child.string:
            string += str(child.string)
    return string

def process_remarks(paragraphs):
    """
    Process the elements with remarks styles
    """
    remark_paragraphs = []
    category = -1

    for paragraph in paragraphs:
        #print('----', paragraph)
        ## if UH_DATU.is_sequence(paragraph):  # is a list
        if isinstance(paragraph, list):
            category, remark_paragraphs = process_remarks(paragraph)
        else:
            paragraph_style = paragraph.get('text:style-name')
            if paragraph_style.startswith(REMARKS_STYLE_NAME_ES) or\
               paragraph_style.startswith(REMARKS_STYLE_NAME_EN):
                category = int(paragraph_style[paragraph_style.rfind('_')+1:])
                #print(paragraph_style.rfind('_'))
                #print("CAT: ", category)
                remark_paragraphs.append(paragraph)

    # convert list of lists in list
    #ret_remark_paragraph = [item for sublist in remark_paragraphs for item in sublist]
    #print('-*-',remark_paragraphs)
    #print('-*-*-',ret_remark_paragraph)
    return category, remark_paragraphs

def main(filename: 'odt file to convert',
         force: ('overwrite existing file', 'flag', 'f')):
    """
    Convert a odt file in HTML educationl package.
    """
    directory_source = unzip_odt(filename)

    file = open(directory_source + "/content.xml", 'r')
    doc = BeautifulSoup(file, "lxml")

    # unit structure
    directory_target = os.path.splitext(filename)[0] + ".mentor"

    if os.path.exists(directory_target) and force:
        shutil.rmtree(directory_target)
    elif os.path.exists(directory_target):
        if not UH_CLIU.query_yes_no("Do you want overwrite the file " + directory_target + "?",
                                    "no"):
            exit(-1)  # exit with error -1
        else:
            shutil.rmtree(directory_target)

    os.makedirs(directory_target)

    chapters = []
    footnotes = []

    # get styles
    style_list = doc.findAll('style:style')
    list_style_list = doc.findAll('text:list-style')
    processor = mentor.ElementProcessor(directory_target, style_list, list_style_list)

    # only styles which style:parent-style-name is Heading_20_X where X is in [1..10]
    #style_list = doc.findAll('style:style')
    #for heading_level in range(1, 10):
    #    styles[str(heading_level)] = create_styles_for_level(heading_level, style_list)

    # getting & classifying all the content from the first heading level 1
    office_text = doc.find('office:text')
    body_text = False
  ###  idx_block = 0

    for child in office_text.children:
        if not body_text and (child.name != "text:h" or
                              not mentor.ElementProcessor.has_string(child)):
            continue
        body_text = True

        try:
            mentor_object = processor.process_element(child)
            if mentor_object is None:
                continue
            if isinstance(mentor_object, mentor.Chapter):
                chapters.append(mentor_object)
                footnotes.append([])
            else:
                chapters[-1].inner_objects.append(mentor_object)
                footnotes_objects = processor.get_inner_mentor_objects_by_type(
                    mentor_object, mentor.Footnote)
                footnotes[-1].extend([foot for foot in footnotes_objects if foot != []])
        except IndexError:
            print("\nError 2: It is not possible to assign the element to a block.",
                  "In the document there must be at least one Heading 1 and",
                  "has to be above the rest of the content.")
            exit(-2)

    # generating level 1 blocks: chapters
    loader = TemplateLoader(os.path.join(os.path.dirname(__file__), 'templates/basic'),
                            auto_reload=True)
    tmpl = loader.load('chapter.html')

    for idx, block in enumerate(chapters, start=1):
        filename_unit = directory_target + "/l1_" + str(idx) + "/chapter.html"
        with open(filename_unit, 'w') as file_block:
            file_block.write(tmpl.generate(title=block.get_string(),
                                           lang="es",
                                           chapters=chapters,
                                           content=block.inner_objects,
                                           footnotes=footnotes[idx-1])
                             .render('html', doctype='html5'))


    # copy Bootstrap files
    UH_OSU.copytree('./bootstrap', directory_target)

    # copy ccs template files
    UH_OSU.copytree('./templates/basic/css', directory_target + "/css")

    # copy js template files
    UH_OSU.copytree('./templates/basic/js', directory_target + "/js")

    return


if __name__ == "__main__":
    plac.call(main)
