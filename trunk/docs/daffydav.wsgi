#!/usr/bin/env python
# encoding: utf-8
"""
daffydav.wsgi

Created by Matteo Pillon on 2009-08-20.
Copyright (c) 2009 Matteo Pillon. All rights reserved.

For running in apache mod_wsgi
"""

config_file = 'config/paste.ini'
from paste.deploy import loadapp
application = loadapp('config:' + config_file)
