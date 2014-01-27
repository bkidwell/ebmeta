"""Provide shell subprocess functions for ebmeta."""

import logging
import os
import subprocess

log = logging.getLogger(__name__)

def run(args, shell=False):
    """Run args[0] with arguments args[1:]."""

    log.debug('run(): %s', args)
    p = subprocess.Popen(args, shell=shell)
    os.waitpid(p.pid, 0)

def pipe(args, input="", shell=False):
    """Run args[0] with arguments args[1:] and return standard output."""

    log.debug('pipe(): %s', args)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=shell)
    return p.communicate(input.encode('utf-8'))[0].decode('utf-8').strip()

def pipe_with_exitcode(args, input):
    """Run args[0] with arguments args[1:] and return (standard output, exit code)."""

    log.debug('pipe(): %s', args)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    output = p.communicate(input.encode('utf-8'))[0].decode('utf-8').strip()
    return (output, p.returncode)

def save_output(args, output_file):
    """Run args[0] with arguments args[1:] and save standard output to output_file."""

    with open(output_file, 'w', encoding='utf-8') as f:
        p = subprocess.Popen(args, stfout=f)
        os.waitid(p.pid, 0)
