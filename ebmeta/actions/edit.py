"""Edit metadata using zenity."""

from bs4 import BeautifulSoup, Tag
import logging
import yaml
from zipfile import ZipFile
import ebmeta
from ebmeta import shell
from ebmeta import template
from ebmeta.actions import backup
from ebmeta.ebook import ebook_factory
from ebmeta.yamlwriter import opf_to_yaml
from ebmeta.zenity import edit_string, ZenityCancelled

log = logging.getLogger(__name__)

def run(arguments=None, new_yaml_text=None):
    """Run this action."""

    path = ebmeta.arguments.filename
    ebook = ebook_factory(path)
    metadata = ebook.get_metadata()
    template_str = template.get_file_content('{}.yaml'.format(ebook.type))
    yaml_text = opf_to_yaml(metadata, template_str)

    if new_yaml_text:
        result = new_yaml_text
    else:
        try:
            result = edit_string(yaml_text, 'Edit Ebook Metadata')
        except ZenityCancelled:
            log.debug('Operation was cancelled.')
            return

    if result == yaml_text.strip():
        log.debug('No change was made.')
    elif result:
        log.debug('Writing changes to ebook file.')
        d1 = yaml.load(yaml_text)
        d2 = yaml.load(result)
        changes = dict()
        for key in d2.keys():
            if key == 'description':
                if (d1[key] or '').strip() != (d2[key] or '').strip(): changes[key] = d2[key]
            if key == 'authors':
                if d1[key] != d2[key]:
                    changes[key] = d2[key]
                    if d2.has_key('author sort'): changes['author sort'] = d2['author sort']
            if key == 'title':
                if d1[key] != d2[key]:
                    changes[key] = d2[key]
                    if d2.has_key('title sort'): changes['title sort'] = d2['title sort']
            else:
                if d1[key] != d2[key]: changes[key] = d2[key]
        log.debug('The following keys changed: %s', ' '.join(changes.keys()))

        backup.run() # backup only if backup doesn't exist

        if ebook.type == 'pdf':
            write_changes_pdf(ebook, changes)
        else:
            write_changes(ebook, changes)

def write_changes(ebook, changes):
    """Write the metadata in the given dictionary into the ebook file."""

    path = ebmeta.arguments.filename

    for key in changes.keys():
        if changes[key] == None: changes[key] = ""

    args = [
        'ebook-meta',
        '"{}"'.format(path)
    ]
    for a, b in (
        ('authors',       'authors'),
        ('book-producer', 'book producer'),
        ('isbn',          'isbn'),
        ('language',      'language'),
        ('date',          'publication date'),
        ('publisher',     'publisher'),
        ('series',        'series'),
        ('title',         'title')
    ):
        if b in changes: args.append('--{}="{}"'.format(a, quote(changes[b])))

    for a, b in (
        ('rating',        'rating'), # rating can't be unset once it's set, from ebook-meta CLI
        ('index',         'series index'), # series index can't be unset either
        ('author-sort',   'author sort'),
        ('title-sort',    'title sort')
    ):
        if b in changes:
            if changes[b]:
                args.append('--{}="{}"'.format(a, quote(changes[b])))

    if 'description' in changes:
        description = shell.pipe(['pandoc'], changes['description'])
        args.append('--comments="{}"'.format(quote(description)))

    if 'tags' in changes:
        args.append('--tags="{}"'.format(quote(','.join(changes['tags']))))

    if len(args) > 2:
        # Run ebook-meta
        shell.pipe(' '.join(args), shell=True)

def quote(text):
    """Change " to \\"."""

    try:
        return text.replace('"', '\\"')
    except TypeError:
        return text

def write_changes_pdf(ebook, changes):
    """Write the metadata in the given dictionary into the pdf file."""

    path = ebmeta.arguments.filename

    for key in changes.keys():
        if changes[key] == None: changes[key] = ""

    args = [
        'exiftool',
        '"{}"'.format(path)
    ]
    for a, b in (
        ('Author', 'authors'),
        ('Title',  'title'),
        ('Description', 'description')
    ):
        if b in changes: args.append('-{}="{}"'.format(a, quote(changes[b])))

    if 'tags' in changes:
        args.append('-Keywords=""')
        for tag in changes['tags']:
            args.append('-Keywords+="{}"'.format(quote(tag)))

    if len(args) > 2:
        # Run ebook-meta
        shell.pipe(' '.join(args), shell=True)
