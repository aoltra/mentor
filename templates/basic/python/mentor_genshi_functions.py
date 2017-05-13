"""
Genshi functions for basic template
"""
from genshi.builder import Element

def create_headers_html(level, content):
    """
    Create internal headers of block (Heading 2 to Heading 10 in odt)
    It uses h1 to h10 html headers
    """
    return Element('h' + str(level-1), class_='section-header-l' + str(level-1))(content)
