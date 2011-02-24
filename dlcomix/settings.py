#!/usr/bin/python
# *-* coding: utf-8 *-*

import os

_DEFAULT_CONFIG = {'PATH' : os.path.expanduser ('~')+'/.dlcomix',
                   'ARCHIVE' : False,
                   'FULL' : False,
                   'USE_COMIX' : False,
                   'LIMIT': 10
                  }

def read_settings(filename):
    context = _DEFAULT_CONFIG.copy()
    if filename:
        tempdict = {}
        execfile(filename, tempdict)
        for key in tempdict:
            if key.isupper():
                context[key] = tempdict[key]
    return context
