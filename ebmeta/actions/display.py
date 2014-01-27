"""Display metadata for FILE."""

import logging
from ebmeta.ebook import ebook_factory

log = logging.getLogger(__name__)

def run(arguments):
    """Run this action."""

    path = arguments.filename
    ebook = ebook_factory(path)

    width = 0
    m = ebook.get_metadata()
    for key in m.keys():
        if len(key) > width:
            width = len(key)
    width += 1

    for key, value in ebook.get_metadata().items():
        if isinstance(value, str):
            value_txt = value
        elif isinstance(value, list):
            value_txt = '; '.join(value)
        else:
            value_txt = repr(value)
        print(key + ':' + (' ' * (width - len(key))) + value_txt)
