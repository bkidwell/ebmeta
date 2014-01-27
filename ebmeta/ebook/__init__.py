"""Methods for manipulating an ebook file."""

import logging

log = logging.getLogger(__name__)

class Ebook(object):
    def __init__(self, path):
        self.path = path

    def get_metadata(self):
        raise NotImplementedError()

# Factory function:

from . import epub
from . import mobi
from . import pdf

def ebook_factory(path):
    ext = path.split('.')[-1].lower()

    logging.debug('filename extension: %s', ext)
    if ext == 'epub': return epub.Epub(path)
    if ext == 'mobi': return mobi.Mobi(path)
    if ext == 'az3': return mobi.Mobi(path)
    if ext == 'pdf': return pdf.Pdf(path)

    raise ValueError('Not a supported file type.')
