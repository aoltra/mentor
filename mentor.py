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

def unzip_odt(odt_file):
    """
    unzip de odt file
    """
    directory_to_extract = os.path.splitext(odt_file)[0]
    directory_to_extract += ".mentor"
    zip_ref = zipfile.ZipFile(odt_file, 'r')
    zip_ref.extractall(directory_to_extract)
    zip_ref.close()


def main():
    """
    main function
    """
    unzip_odt("prueba1.zip")
    return



if __name__ == "__main__":
    main()
