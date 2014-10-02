#!/usr/bin/env python

# pylint: disable=missing-docstring

import os


for parent, subdirs, files in os.walk(os.getcwd()):
    for fi in files:
        if fi.endswith('.pyc'):
            true_path = os.path.join(parent, fi)
            print '{} removed'.format(true_path)
            os.remove(true_path)
