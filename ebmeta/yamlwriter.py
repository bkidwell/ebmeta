import re
import logging
from string import Template

log = logging.getLogger(__name__)

yaml_simple = re.compile('^[0-9\.]+$')
yaml_newline = re.compile('^', re.MULTILINE)
def yaml_value(txt, multiline=False):
    if txt == None:
        return '~'
    if len(txt) == 0: return '~'
    if type(txt) is list:
        return '[' + ', '.join(yaml_value(x) for x in txt) + ']'
    if yaml_simple.match(txt): return txt
    if multiline:
        return '|\n' + yaml_newline.sub(' ', txt)
    else:
        return '' + txt + ''

def opf_to_yaml(opf, template_str):
    d = dict()
    for key in opf.keys():
        d[key.replace(' ', '_')] = yaml_value(opf[key], key == 'description')
    log.debug(repr(d))
    return Template(template_str).substitute(d)
