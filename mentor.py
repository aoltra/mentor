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
    if not os.path.exists(directory_target):
        os.makedirs(directory_target)

    blocks_l1 = doc.findAll('text:h', attrs={"text:outline-level" : "1"})
    for i in range(len(blocks_l1)):
        os.makedirs(directory_target + "/l1_" + str(i+1))

    return



if __name__ == "__main__":
    main()
