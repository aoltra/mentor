"""
Conversor de odt a html para incorporarlo en Moodle
"""
#
# Autor: Alfredo Oltra
# Fecha: 3/5/2017
#
# Licencia GPL-3.0

import os
import zipfile
from bs4 import BeautifulSoup
from genshi.template import TemplateLoader

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
    filename = "prueba1.odt"
    directory_source = unzip_odt(filename)

    file = open(directory_source + "/content.xml", 'r')
    doc = BeautifulSoup(file, "lxml")

    # unit structure
    directory_target = os.path.splitext(filename)[0] + ".mentor"
  #  if not os.path.exists(directory_target):
  #      os.makedirs(directory_target)
    if os.path.exists(directory_target):
        shutil.rmtree(directory_target)

    blocks_l1 = doc.findAll('text:h', attrs={"text:outline-level" : "1"})
    for i in range(len(blocks_l1)):
        os.makedirs(directory_target + "/l1_" + str(i+1))


    # generating units
    loader = TemplateLoader(os.path.join(os.path.dirname(__file__), 'templates/basic'),
                            auto_reload=True)
    tmpl = loader.load('unit.html')

    for block in enumerate(blocks_l1):
        print(tmpl.generate(title=block[1].string, lang="es").render('html', doctype='html5'))



    return



if __name__ == "__main__":
    main()
