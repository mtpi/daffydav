#!/usr/bin/env python
# encoding: utf-8
"""
osx.py

Created by Matteo Pillon on 2009-08-11.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from daffydav.authenticators.unix import UnixAuthenticator

import OpenDirectoryAuth

import logging
log = logging.getLogger(__name__)

class OSXAuthenticator(UnixAuthenticator):
    """
    OSXAuthenticator
    
    This authenticator validates user against Mac OS X Open Directory
    """
    
    def _validate(self):
        return OpenDirectoryAuth.authenticate(self.username, self.password)
