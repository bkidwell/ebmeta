"""Backup FILE to an embedded file inside FILE."""

import logging
import os
import os.path
import shutil
import ebmeta

log = logging.getLogger(__name__)

def run():
    """Run this action."""

    path = ebmeta.arguments.filename
    abspath = os.path.abspath(path)
    folder = os.path.dirname(abspath)

    backup_folder = os.path.join(folder, '.backup')
    backup_path = os.path.join(
        backup_folder, os.path.basename(path) + '.backup'
    )

    if os.path.exists(backup_path):
        log.debug('Skipping backup because a backup was found in "{}".'.format(backup_path))
        return

    if not os.path.exists(backup_folder):
        os.mkdir(backup_folder)

    shutil.copy2(abspath, backup_path)
    log.debug('Wrote backup file to "{}".'.format(backup_path))
