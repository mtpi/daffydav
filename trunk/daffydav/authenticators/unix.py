#!/usr/bin/env python
# encoding: utf-8
"""
unix.py

From pyftpdlib project
"""

from daffydav.authenticators import Authenticator

import pwd, os

import logging
log = logging.getLogger(__name__)

class UnixAuthenticator(Authenticator):
    """
    UnixAuthenticator
    
    This authenticator is the base for unix family authenticators, has no validation function
    """
    
    def get_home_dir(self):
        return pwd.getpwnam(self.username).pw_dir
    
    def _impersonate_user(self):
        uid = pwd.getpwnam(self.username).pw_uid
        gid = pwd.getpwnam(self.username).pw_gid
        os.setegid(gid)
        os.seteuid(uid)
    
    def _terminate_impersonation(self):
        os.setegid(os.getgid())
        os.seteuid(os.getuid())
