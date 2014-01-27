"""Ebook metadata."""

from lxml import etree
import re
import logging
from ebmeta import shell

log = logging.getLogger(__name__)

months = u"Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sept,Oct,Nov,Dec".split(',')
nsmap = {
    'opf': 'http://www.idpf.org/2007/opf',
    'dc': 'http://purl.org/dc/elements/1.1/'
}

def get_first(element, query):
    e = element.xpath(query, namespaces=nsmap)
    if len(e) > 0:
        return e[0]
    else:
        return None

def get_attr(element, attr, query=None):
    if query == None:
        e = element
    else:
        e = get_first(element, query)
    try:
        return e[attr]
    except AttributeError:
        return None
def get_str(element, query):
    e = get_first(element, query)
    try:
        return e.text
    except TypeError:
        return None

isodate = re.compile("([\d]+)-([\d]+)-([\d]+)")
def formatDate(txt):
    if not txt: return None
    m = isodate.match(txt)
    if not m: return None
    return u" ".join((
        m.group(3),
        months[int(m.group(2)) - 1],
        m.group(1)
    ))

def htmlToMarkdown(txt):
    if not txt: return txt
    return shell.pipe(["pandoc", "--no-wrap", "--from", "html", "--to", "markdown"], txt).strip()

class Opf(dict):
    def __init__(self, txt):
        if not (txt[:100].find("<?xml") >= 0):
            raise ValueError("Not an XML stream.")

        package = etree.fromstring(txt.encode('utf-8'))
        metadata = package.xpath

        self['title'] = get_str(metadata, 'dc:title')
        self['title sort'] = get_attr(metadata, 'content', 'meta[@calibre:title_sort]')

        authors = metadata.xpath('dc:creator[@opf:role = "aut" or @role = "aut"]')
        if authors and len(authors):
            self['authors'] = ' & '.join(
                [x for x in [author.text for author in authors] if x is not None]
            )
            self['author sort'] = (
                get_attr(authors[0], 'opf:role') or
                get_attr(authors[0], 'file-as')
            )

        self['publication date'] = formatDate(get_str(metadata, 'dc:date'))
        self['publisher'] = get_str(metadata, 'dc:publisher')
        self[u'book producer'] = (
            getStr( soup.find('dc:contributor', attrs={'opf:role':'bkp'}) ) or
            getStr( soup.find('dc:contributor', attrs={'role':'bkp'}) )
        )
        self[u'isbn'] = (
            getStr( soup.find('dc:identifier', attrs={'opf:scheme':'ISBN'}) ) or
            getStr( soup.find('dc:identifier', attrs={'opf:scheme':'isbn'}) ) or
            getStr( soup.find('dc:identifier', attrs={'scheme':'ISBN'}) ) or
            getStr( soup.find('dc:identifier', attrs={'scheme':'isbn'}) )
        )
        if not self[u'isbn']:
            for bookid in [getStr(x) for x in soup.findAll('dc:identifier')]:
                if bookid and ('isbn' in bookid.lower()):
                    self[u'isbn'] = bookid.split(':')[-1]
        self[u'language'] = getStr(soup.find('dc:language'))
        self[u'rating'] = getAttr(soup.find('meta', attrs={'name':'calibre:rating'}), 'content')
        self[u'series'] = getAttr(soup.find('meta', attrs={'name':'calibre:series'}), 'content')
        self[u'series index']  = getAttr(soup.find('meta', attrs={'name':'calibre:series_index'}), 'content')
        self[u'uuid'] = (
            getStr(soup.find('dc:identifier', attrs={'opf:scheme':'uuid'})) or
            getStr(soup.find('dc:identifier', attrs={'opf:scheme':'UUID'})) or
            getStr(soup.find('dc:identifier', attrs={'scheme':'uuid'})) or
            getStr(soup.find('dc:identifier', attrs={'scheme':'UUID'}))
        )
        tags = soup.findAll('dc:subject')
        self[u'tags'] = []
        if tags:
            self[u'tags'] = [getStr(x) for x in tags]
            #self['tags'] = ", ".join([getStr(x) for x in tags])
        description = getStr(soup.find('dc:description'))
        self[u'description'] = htmlToMarkdown(description)

    def __unicode__(self):
        txt = []
        key_width = 0
        keys = self.keys()
        keys.sort()

        for key in keys:
            if len(key) > key_width: key_width = len(key)

        for key in keys:
            if key == 'tags': value = u", ".join(self[u'tags'])
            else: value = self[key]

            #print "key: " + key.__class__.__name__ + " : " + key
            #print "value: " + value.__class__.__name__
            txt.append(u"{}: {}".format(key.ljust(key_width, u' '), value))

        return u"\n".join(txt)
