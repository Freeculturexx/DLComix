import os

_DEFAULT_CONFIG ={'COMIC' : 'garfield',
                    'PATH' : os.path.expanduser ("~" )+'/.dlcomix/',
                    'ARCHIVE' : False,
                    'FULL' : False,
}

def read_settings(filename):
    """Load a Python file into a dictionary.
"""
    context = _DEFAULT_CONFIG.copy()
    if filename:
        tempdict = {}
        execfile(filename, tempdict)
        for key in tempdict:
            if key.isupper():
                context[key] = tempdict[key]
    return context