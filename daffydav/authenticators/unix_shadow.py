#!/usr/bin/env python
# encoding: utf-8
"""
unix_shadow.py

Created by Matteo Pillon on 2009-08-13.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from daffydav.authenticators.unix import UnixAuthenticator

import spwd, crypt

import logging
log = logging.getLogger(__name__)

class ShadowUnixAuthenticator(UnixAuthenticator):
    """
    ShadowUnixAuthenticator
    
    This authenticator validates user against Unix passwd/shadow
    """
    
    def _validate(self):
        pw1 = spwd.getspnam(self.username).sp_pwd
        pw2 = crypt.crypt(self.password, pw1)
        return pw1 == pw2
