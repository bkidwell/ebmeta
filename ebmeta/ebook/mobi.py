import logging
import tempfile
from ebmeta import shell
from ebmeta.formats.opfreader import OpfReader
from . import Ebook

log = logging.getLogger('mobi')

class Mobi(Ebook):
    def __init__(self, path):
        self.type = 'mobi'
        self.__opf = None
        super(Mobi, self).__init__(path)

    def get_metadata(self):
        if self.__opf:
            return self.__opf

        with tempfile.NamedTemporaryFile() as f:
            shell.pipe(["ebook-meta", "--to-opf=" + f.name, self.path])
            opf_str = f.read().decode('utf-8')

        self.__opf = OpfReader(opf_str)
        return self.__opf
