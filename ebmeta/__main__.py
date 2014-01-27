"""`ebmeta` is a tool for editing metadata in ebook file."""

import logging
import ebmeta

def main():
    ebmeta.init()
    log = logging.getLogger(__name__)

    log.debug('Arguments: %s', repr(ebmeta.arguments))
    if ebmeta.arguments:
        getattr(ebmeta.actions, ebmeta.arguments.action).run(ebmeta.arguments)

if __name__ == '__main__':
    main()
