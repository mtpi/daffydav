#!/usr/bin/env python
# encoding: utf-8
"""
AJAX based file manager

Created by Matteo Pillon on 2009-08-21.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from mako.lookup import TemplateLookup
from paste.fileapp import DirectoryApp

from daffydav.filemanager.backends import FileManagerBackend
from daffydav.filemanager.backends.ajax import actions

import os.path

class AJAXFileManager(FileManagerBackend):
    def __init__(self):
        FileManagerBackend.__init__(self)
        templates_path = os.path.join(os.path.dirname(__file__), 'templates')
        resources_path = os.path.join(os.path.dirname(__file__), 'resources')
        self.templatelookup = TemplateLookup(directories=[templates_path])
        self.real_resources_app = DirectoryApp(resources_path)
        self.actions = {}
        for action in actions.__all__:
            self.actions[action] = eval('actions.'+action)
