import logging
import tempfile
from zipfile import ZipFile
from ebmeta import shell
from ebmeta.formats.opfreader import OpfReader
from . import Ebook

log = logging.getLogger('epub')

class Epub(Ebook):
    def __init__(self, path):
        self.type = 'epub'
        self.__opf = None
        super(Epub, self).__init__(path)

    def get_metadata(self):
        if self.__opf:
            return self.__opf

        opf_str = None

        try:
            with ZipFile(self.path, 'r') as zip:
                try:
                    opf_str = zip.read('content.opf').decode('utf-8')
                except KeyError:
                    opf_str = zip.read('OEBPS/content.opf').decode('utf-8')
        except:
            pass

        # give up and use the ebook-meta to get the metadata
        if opf_str is None:
            with tempfile.NamedTemporaryFile() as f:
                shell.pipe(["ebook-meta", "--to-opf=" + f.name, self.path])
                opf_str = f.read().decode('utf-8')

        self.__opf = OpfReader(opf_str)
        return self.__opf
