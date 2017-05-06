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
import Chapter


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

    blocks_l1 = []

    blocks = (block for block in doc.findAll('text:h', attrs={"text:outline-level" : "1"})
              if block.string)
    for idx, block in enumerate(blocks, start=1):
        os.makedirs(directory_target + "/l1_" + str(idx))
        blocks_l1.append(Chapter.Chapter(idx, block))

    blocks = []

    # generating level 1 blocks
    loader = TemplateLoader(os.path.join(os.path.dirname(__file__), 'templates/basic'),
                            auto_reload=True)
    tmpl = loader.load('chapter.html')

    for idx, block in enumerate(blocks_l1, start=1):
        filename_unit = directory_target + "/l1_" + str(idx) + "/chapter.html"
        with open(filename_unit, 'w') as file_block:
            file_block.write(tmpl.generate(title=block.block.string,
                                           lang="es",
                                           blocks=blocks_l1).render('html', doctype='html5'))


    # copy Bootstrap files
    UH_OSU.copytree('./bootstrap', directory_target)

    # copy ccs template files
    UH_OSU.copytree('./templates/basic/css', directory_target + "/css")

    return


if __name__ == "__main__":
    plac.call(main)
