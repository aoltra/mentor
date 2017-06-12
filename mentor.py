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


def create_styles_for_level(level_number, style_list):
    """
    Create a list of heading styles
    """
    style_name = "Heading_20_" + str(level_number)

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

def has_string(tag):
    """
    Return true if the tag has a string
    """
    for child in tag.children:
        if child.string:
            return True
    return False

def get_string_from_tag(tag):
    """
    Get the string of the tag, joining the strings of its children
    """
    string = ""
    for child in tag.children:
        if child.string:
            string += str(child.string)
    return string

def get_inner_paragraphs(tag):
    """
    Return a list of children paragraphs of tag.
    """
    paragraph_list = []
    for child in tag.children:
        if child.name == 'text:p':
            paragraph_list.append(child)
        else:
            inner_paragraphs = get_inner_paragraphs(child)
            for item in inner_paragraphs:
                paragraph_list.append(item)

    return paragraph_list

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

    styles = {"1":[], "2":[], "3":[], "4":[], "5":[], "6":[], "7":[], "8":[], "9":[], "10":[]}
    blocks_l1 = []

    # only styles which style:parent-style-name is Heading_20_X where X is in [1..10]
    style_list = doc.findAll('style:style')
    for heading_level in range(1, 10):
        styles[str(heading_level)] = create_styles_for_level(heading_level, style_list)

    # getting & classifying all the content from the first heading level 1
    office_text = doc.find('office:text')
    body_text = False
    idx_block = 0
    for child in office_text.children:
        if not body_text and (child.name != "text:h" or not has_string(child)):
            continue
        body_text = True
        child_style = child.get('text:style-name')

        # headings not empty
        if child.name == "text:h" and has_string(child):
            #print(child)

            if child_style in styles["1"]:
                idx_block += 1
                os.makedirs(directory_target + "/l1_" + str(idx_block))
                blocks_l1.append(mentor.Block(idx_block, child))
                continue
            else:
                try:
                    blocks_l1[-1].content.append(mentor.Heading(int(get_level_number(child_style,
                                                                                     styles)),
                                                                get_string_from_tag(child)))
                    continue
                except IndexError:
                    print("\nError 2: In the document there must be at least one Heading 1 and",
                          "has to be above the rest of the headings.")
                    exit(-2)

            # if child_style.startswith(REMARKS_STYLE_NAME_ES) or\
            #    child_style.startswith(REMARKS_STYLE_NAME_EN):
            #     try:
            #         print(child_style)
            #         print(int(child_style[-child_style.rfind('_'):]))
            #         blocks_l1[-1].content.append(mentor.Remarks(1, get_string_from_tag(child)))
            #     except IndexError:
            #         print("\nError 5: It is not possible to assign the remarks content to a",
            #               "block. In the document there must be at least one Heading 1 and",
            #               "has to be above the rest of the content.")
            #         exit(-5)

                        # if child.name == "text:p" and has_string(child):
                        #     try:
                        #         blocks_l1[-1].content.append(mentor.Paragraph(get_string_from_tag(child)))
                        #         continue
                        #     except IndexError:
                        #         print("\nError 4:  It is not possible to assign the paragraph to a block.",
                        #               "In the document there must be at least one Heading 1 and",
                        #               "has to be above the rest of the content.")
                        #         exit(-4)

        cokik = mentor.ElementProcessor.process_element(child)
        if cokik is not None:
            blocks_l1[-1].content.append(cokik)

        # elements not included in previous controls
        # Remarks
        # inner_paragraphs = get_inner_paragraphs(child)
        # if inner_paragraphs:
        #     category, remark_paragraphs = process_remarks(inner_paragraphs)
        #     if remark_paragraphs:
        #         blocks_l1[-1].content.append(mentor.Remark(category, remark_paragraphs))
        #         continue


    # for block in enumerate(blocks_l1):
    #     for sec in enumerate(block[1].content):
    #         print(sec)

    # generating level 1 blocks
    loader = TemplateLoader(os.path.join(os.path.dirname(__file__), 'templates/basic'),
                            auto_reload=True)
    tmpl = loader.load('chapter.html')

    for idx, block in enumerate(blocks_l1, start=1):
        filename_unit = directory_target + "/l1_" + str(idx) + "/chapter.html"
        with open(filename_unit, 'w') as file_block:
           # print(block.content)
            file_block.write(tmpl.generate(title=block.get_string(),
                                           lang="es",
                                           blocks=blocks_l1,
                                           content=block.content)
                             .render('html', doctype='html5'))


    # copy Bootstrap files
    UH_OSU.copytree('./bootstrap', directory_target)

    # copy ccs template files
    UH_OSU.copytree('./templates/basic/css', directory_target + "/css")

    return


if __name__ == "__main__":
    plac.call(main)
