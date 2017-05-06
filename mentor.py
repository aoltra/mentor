"""
Conversor de odt a html para incorporarlo en Moodle
"""
#
# Author: Alfredo Oltra
# Date: 3/5/2017
#
# License GPL-3.0

import os
import zipfile
from bs4 import BeautifulSoup
from genshi.template import TemplateLoader

import Chapter

# a eliminar en un futuro
import shutil

def unzip_odt(odt_file):
    """
    unzip de odt file
    """
    directory_to_extract = os.path.splitext(odt_file)[0]
    directory_to_extract += ".mentor.tmp"
    zip_ref = zipfile.ZipFile(odt_file, 'r')
    zip_ref.extractall(directory_to_extract)
    zip_ref.close()
    return directory_to_extract



def main():
    """
    main function
    """
    filename = "Unit 11. Computer Networks (I).odt"
    directory_source = unzip_odt(filename)

    file = open(directory_source + "/content.xml", 'r')
    doc = BeautifulSoup(file, "lxml")

    # unit structure
    directory_target = os.path.splitext(filename)[0] + ".mentor"
  #  if not os.path.exists(directory_target):
  #      os.makedirs(directory_target)
  #  if os.path.exists(directory_target):
  #      shutil.rmtree(directory_target)

    blocks_l1 = []

    blocks = doc.findAll('text:h', attrs={"text:outline-level" : "1"})
    for idx, block in enumerate(blocks, start=1):
        os.makedirs(directory_target + "/l1_" + str(idx))
        blocks_l1.append(Chapter.Chapter(idx, block))

    blocks = []

    # generating units
    loader = TemplateLoader(os.path.join(os.path.dirname(__file__), 'templates/basic'),
                            auto_reload=True)
    tmpl = loader.load('chapter.html')

    for idx, block in enumerate(blocks_l1, start=1):
        filename_unit = directory_target + "/l1_" + str(idx) + "/chapter.html"
        with open(filename_unit, 'w') as file_unit:
            file_unit.write(tmpl.generate(title=block.block.string,
                                          lang="es", uts=blocks_l1).render('html', doctype='html5'))

    return


if __name__ == "__main__":
    main()
