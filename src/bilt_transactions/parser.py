#
# Parse an MHTML file containing Bilt card transactions, print the
# transactions in CSV format
#

import re
from unmhtml import MHTMLConverter

def extract_paragraphs(fn: str):
    '''
    Return the contents of all the <P> elements in an MHTML file.

    Arguments:
        fn:  the name of the file
    '''
    converter = MHTMLConverter()
    html = converter.convert_file(fn)
    return re.findall(r'<p class.*?</p>', html)


