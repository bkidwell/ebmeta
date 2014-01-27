"""PDF metadata from exiftool command."""

import logging
import json

log = logging.getLogger(__name__)

class ExifToolJsonReader(dict):
    def __init__(self, txt):
        super().__init__()

        if not (len(txt)):
            raise ValueError('No input.')

        self['authors'] = None
        self['title'] = None
        self['tags'] = []
        self['description'] = None

        data = json.loads(txt)[0]
        for key, value in data.items():
            if key == 'Author':
                self['authors'] = value
            if key == 'Title':
                self['title'] = value
            if key == 'Keywords':
                self['tags'] = value
            if key == 'Description':
                self['description'] = value
