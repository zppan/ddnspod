﻿#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import sys
import logging
from dnspodapi import main

logging.basicConfig(level=logging.INFO)

# If we are running from a wheel, add the wheel to sys.path
# This allows the usage python pip-*.whl/pip install pip-*.whl
print __package__
if __package__ == '':
    # __file__ is pip-*.whl/pip/__main__.py
    # first dirname call strips of '/__main__.py', second strips off '/pip'
    # Resulting path is the name of the wheel itself
    # Add that to sys.path so we can import pip
    #path = os.path.dirname(os.path.dirname(__file__))
    #sys.path.insert(0, path)
    pass

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        main('./config.json')
