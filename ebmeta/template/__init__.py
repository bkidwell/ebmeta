"""Module containing template files used in ebmeta output."""

import pkgutil

def get_file_content(filename):
    """Get contents of file named by filename, in template package."""

    return pkgutil.get_data(__name__, filename).decode('utf-8')
