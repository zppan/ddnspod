#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import sys

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        ddns = DDnspod(getIDToken(sys.argv[1]),"pi")
    else:
        ddns = DDnspod(getIDToken(),"pi")
    while True:
        try:
            ip = getip()
            logging.info("IP: %s" % ip)
            if current_ip != ip:
                if ddns.updns(ip):
                    current_ip = ip
                else:
                    logging.info("updnspod error")
        except Exception as e:
            print e
            pass
        time.sleep(60)

from __future__ import absolute_import

import os
import sys

# If we are running from a wheel, add the wheel to sys.path
# This allows the usage python pip-*.whl/pip install pip-*.whl
if __package__ == '':
    # __file__ is pip-*.whl/pip/__main__.py
    # first dirname call strips of '/__main__.py', second strips off '/pip'
    # Resulting path is the name of the wheel itself
    # Add that to sys.path so we can import pip
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

import pip  # noqa

if __name__ == '__main__':
    sys.exit(pip.main())
