#!/usr/bin/env python
# encoding: utf-8
"""
templating.py

Created by Matteo Pillon on 2009-08-21.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from paste.deploy import CONFIG

def render(templatename):
    return CONFIG['filemanager_backend'].render(templatename)
