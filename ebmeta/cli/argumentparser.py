import argparse
import logging
import ebmeta

log = logging.getLogger(__name__)

help_txt = """\
ebmeta is a tool for editing metadata in a ebook files (Epub,
Mobipocket, or PDF).
"""

epilog = """\
actions:
  backup    Backup FILE to an ./.backup/FILE.backup
  display   Display metadata from FILE
  edit      Edit metadata using zenity
  reset     Reset metadata back to what it was before the first edit
  version   Print ebmeta version number
"""


def setup_args(parser):
    """Adds ebmeta argument structure to an instance of ArgumentParser.
    :rtype : None
    """

    parser.add_argument(
        'action', nargs='?', metavar='action',
        choices=['backup', 'display', 'edit', 'reset', 'version'],
        help='Which action to perform.'
    )
    parser.add_argument(
        'filename', nargs='?', metavar='FILE',
        help='Path to an ebook file.'
    )


class ArgumentParser(argparse.ArgumentParser):
    """Extend argparse.ArgumentParser with the argument structure for ebmeta."""

    def __init__(self):
        super().__init__(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=help_txt, epilog=epilog, prog=ebmeta.PROGRAM_NAME
        )
        setup_args(self)
        log.debug(repr(self))
