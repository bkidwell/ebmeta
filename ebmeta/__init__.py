"""ebmeta package"""

VERSION = '0.2'
PROGRAM_NAME = 'ebmeta'

arguments = None
log = None

import logging
from . import actions
from ebmeta.cli.argumentparser import ArgumentParser
import sys

def init():
    """Initialize ebmeta package."""

    global arguments
    global log

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)

    arguments = ArgumentParser().parse_args()
