#!/usr/bin/env python
# encoding: utf-8
"""
linux_pam.py

Created by Matteo Pillon on 2009-08-13.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from daffydav.authenticators.unix import UnixAuthenticator

import logging
log = logging.getLogger(__name__)

class LinuxPAMAuthenticator(UnixAuthenticator):
    """
    LinuxPAMAuthenticator
    
    Use Linux PAM auth mechanism to validate users
    """
    
    def _validate(self):
        ##TODO: not implemented
        return False
