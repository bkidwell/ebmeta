"""Ebook metadata."""

from bs4 import BeautifulSoup
import re
import logging
from ebmeta import shell

log = logging.getLogger(__name__)

months = 'Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sept,Oct,Nov,Dec'.split(',')


def get_attr(soup, attr):
    try:
        return soup[attr]
    except TypeError:
        return None


def get_str(soup):
    try:
        return soup.string
    except AttributeError:
        return None


isodate = re.compile('([\d]+)-([\d]+)-([\d]+)')


def format_date(txt):
    if not txt:
        return None
    m = isodate.match(txt)
    if not m:
        return None
    return ' '.join((
        m.group(3),
        months[int(m.group(2)) - 1],
        m.group(1)
    ))


def html_to_markdown(txt):
    if not txt:
        return txt
    return shell.pipe(['pandoc', '--no-wrap', '--from', 'html', '--to', 'markdown'], txt).strip()


class OpfReader(dict):
    def __init__(self, txt):
        super().__init__()

        if not (txt[:100].find('<?xml') >= 0):
            raise ValueError('Not an XML stream.')

        soup = BeautifulSoup(txt, 'xml')
        metadata = soup.metadata
        self['title'] = get_str(metadata.title)
        self['title sort'] = get_attr(soup.find('meta', attrs={'name': 'title_sort'}), 'content')
        authors = (
            metadata.findAll('creator', attrs={'role': 'aut'})
        )
        self['authors'] = None
        self['author sort'] = None
        if authors and len(authors):
            self['authors'] = ' & '.join([x for x in [get_str(author) for author in authors] if x is not None])
            self['author sort'] = get_attr(authors[0], 'file-as')
        self['publication date'] = format_date(get_str(metadata.find('date')))
        self['publisher'] = get_str(metadata.find('publisher'))
        self['book producer'] = get_str(metadata.find('dc:contributor', attrs={'role': 'bkp'}))
        self['isbn'] = (
            get_str(metadata.find('identifier', attrs={'scheme': 'ISBN'})) or
            get_str(metadata.find('identifier', attrs={'scheme': 'isbn'}))
        )
        if not self['isbn']:
            for bookid in [get_str(x) for x in metadata.findAll('identifier')]:
                if bookid and ('isbn' in bookid.lower()):
                    self['isbn'] = bookid.split(':')[-1]
        self['language'] = get_str(metadata.find('language'))
        self['rating'] = get_attr(soup.find('meta', attrs={'name': 'rating'}), 'content')
        self['series'] = get_attr(soup.find('meta', attrs={'name': 'series'}), 'content')
        self['series index'] = get_attr(soup.find('meta', attrs={'name': 'series_index'}), 'content')
        self['uuid'] = (
            get_str(metadata.find('identifier', attrs={'scheme': 'uuid'})) or
            get_str(metadata.find('identifier', attrs={'scheme': 'UUID'}))
        )
        tags = metadata.findAll('subject')
        self['tags'] = []
        if tags:
            self['tags'] = [get_str(x) for x in tags]
        description = get_str(metadata.find('description'))
        self['description'] = html_to_markdown(description)

    def __str__(self):
        txt = []
        key_width = 0
        keys = sorted(self.keys())

        for key in keys:
            if len(key) > key_width:
                key_width = len(key)

        for key in keys:
            if key == 'tags':
                value = ', '.join(self['tags'])
            else:
                value = self[key]

            txt.append('{}: {}'.format(key.ljust(key_width, ' '), value))

        return '\n'.join(txt)
