import logging
from ebmeta import shell
from ebmeta.formats.exiftooljsonreader import ExifToolJsonReader
from . import Ebook

log = logging.getLogger('pdf')

class Pdf(Ebook):
    def __init__(self, path):
        self.type = 'pdf'
        self.__pdfmeta = None
        super(Pdf, self).__init__(path)

    def get_metadata(self):
        if self.__pdfmeta:
            return self.__pdfmeta

        pdfmeta_txt = shell.pipe(['exiftool', '-json', self.path])
        self.__pdfmeta = ExifToolJsonReader(pdfmeta_txt)
        return self.__pdfmeta
