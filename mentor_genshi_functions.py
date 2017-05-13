"""
funciones genshi
"""
from genshi.builder import Element

def create_headers_html(level, content):
   # return '<h' + str(level-1) + ' class="section-header-l' + str(level-1) +\
   #  '">' + string  + '</h' + str(level-1) +'>'
    return Element('h' + str(level-1), class_='section-header-l' + str(level-1))(content)