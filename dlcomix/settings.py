import os

_DEFAULT_CONFIG ={'PATH' : os.path.expanduser ("~" )+'/.dlcomix/download/',
                    'ARCHIVE' : False,
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