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
    level_number = list([key for key, value in styles.items() if level_style in value])
    if not level_number:
        print("Error 3: Style not found.")
        exit(-3)

    return int(level_number[0])

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

    # only styles which style:parent-style-name is Heading_20_1
    style_list = doc.findAll('style:style')
    styles["1"] = create_styles_for_level(1, style_list)
    styles["2"] = create_styles_for_level(2, style_list)
    styles["3"] = create_styles_for_level(3, style_list)

    # getting & classifying all the content from the first header level 1
    office_text = doc.find('office:text')
    body_text = False
    idx_block = 0
    for child in office_text.children:
        if not body_text and (child.name != "text:h" or not child.string):
            continue
        body_text = True

        # headers not empty
        if child.name == "text:h" and child.string:
            level_style = child['text:style-name']

            if level_style in styles["1"]:
                idx_block += 1
                os.makedirs(directory_target + "/l1_" + str(idx_block))
                blocks_l1.append(mentor.Block(idx_block, child))
            else:
                try:
                    blocks_l1[-1].content.append(mentor.Header(int(get_level_number(level_style,
                                                                                    styles)),
                                                               child.string))
                except IndexError:
                    print("\nError 2: In the document there must be at least one Heading 1 and",
                          "has to be above the rest of the headings.")
                    exit(-2)


    for block in enumerate(blocks_l1):
        for sec in enumerate(block[1].content):
            print(sec)

    # generating level 1 blocks
    loader = TemplateLoader(os.path.join(os.path.dirname(__file__), 'templates/basic'),
                            auto_reload=True)
    tmpl = loader.load('chapter.html')

    for idx, block in enumerate(blocks_l1, start=1):
        filename_unit = directory_target + "/l1_" + str(idx) + "/chapter.html"
        with open(filename_unit, 'w') as file_block:
            file_block.write(tmpl.generate(title=block.block.string,
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
