"""PDF metadata from pdftk command."""

import logging

log = logging.getLogger(__name__)

class PdfTkReader(dict):
    def __init__(self, txt):
        super().__init__()

        if not (len(txt)):
            raise ValueError('No input.')

        back1 = ''
        back2 = ''
        data = dict()
        for line in txt.splitlines(False):
            if back2 == 'InfoBegin':
                if back1[:9] == 'InfoKey: ':
                    if line[:11] == 'InfoValue: ':
                        data[back1[9:]] = line[11:]
            back2 = back1
            back1 = line

        log.debug('keys: ' + repr(data))
