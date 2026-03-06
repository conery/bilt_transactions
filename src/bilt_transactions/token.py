#
# Token
#

import calendar
from datetime import datetime
import re

class Token:

    months = tuple(calendar.month_name[1:])

    def __init__(self, p):
        '''
        Create a token from a paragraph element
        '''
        self.src = p
        content = re.match(r'<p class.*>(.*)</p>', p).group(1)
        if content.startswith(self.months) and re.match(r'\w+ \d{1,2}, \d{4}', content):
            self.kind = 'date'
            self.value = datetime.strptime(content, "%B %d, %Y").date()
        elif m := re.match(r'(\d+\.\d\d)', re.sub(r'[,$-]','',content)):
            self.kind = 'amount'
            self.value = float(m.group(1))
            if content.startswith('-'):
                self.value = -self.value
        else:
            self.kind = 'description'
            self.value = content

