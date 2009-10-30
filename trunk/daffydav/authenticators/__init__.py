"""
Authentication backends

Created by Matteo Pillon on 2009-08-13.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

import logging
log = logging.getLogger(__name__)

from threading import Lock
from daffydav.lib.registry import authenticator
from webob import exc

from paste.deploy import CONFIG

class AuthDaemon(object):
    """
    This objects helds some informations needed to instantiate
    an Authenticator object on every request
    """
    def __init__(self, authenticator, authenticator_options):
        self.authenticator = authenticator
        self.authenticator_options = authenticator_options
        self.impersonation_lock = Lock()
    
    def authfunc(self, environ, username, password):
        """
        Create a new authenticator instance (which one is configured)
        and return what validate method says
        """
        environ['paste.registry'].register(authenticator, self.authenticator(self, username, password,
            **self.authenticator_options))
        return authenticator.validate()

class Authenticator(object):
    """
    Dummy Authenticator backend, has to be subclassed to add some functionality
    Some functions are inspired from pyftpdlib project
    
    All these locking stuff is here because any changes in EUID/EGID is shared
    between all the threads (as the change take place in the process containing them).
    So we need to make sure only one thread at a time uses the *validate* or
    *run_as* functions.
    """
    
    # if it authenticates virtual user, no need for locking and run_as_current_user
    virtual = False
    
    def __init__(self, authdaemon, username, password):
        """Init authenticator module, can accept some options as keyword arguments"""
        self.authdaemon = authdaemon
        self.username = username
        self.password = password
    
    def validate(self):
        """Validate user identity"""
        with self.authdaemon.impersonation_lock:
            rv = self._validate()
        return rv
    
    def _validate(self):
        """
        Validate if given self.username and self.password identify a valid user
        WARNING: as it usually requires root privileges, it needs locking (provided in validate)
        """
        return False
    
    def get_home_dir(self):
        """Get home directory for the specified user"""
        return ''
    
    def _impersonate_user(self):
        """
        Become real system user in order (for file access restriction)
        WARNING: not thread-safe, it needs locking (provided in run_as_current_user)
        """
        pass
        
    def _terminate_impersonation(self):
        """Come back to deamon user"""
        pass
    
    def run_as_current_user(self, function, *args, **kwargs):
        """Execute a function impersonating the current logged-in user."""
        if self.virtual:
            return function(*args, **kwargs)
        self.authdaemon.impersonation_lock.acquire()
        self._impersonate_user()
        try:
            rv = function(*args, **kwargs)
        finally:
            self._terminate_impersonation()
            self.authdaemon.impersonation_lock.release()
        return rv
    
    def logout(self, username):
        """
        Return an HTTPUnauthorized if logged in user is username
        """
        if self.username == username:
            raise exc.HTTPUnauthorized(explanation='logout', headers={'WWW-Authenticate':'Basic realm="%s"' % CONFIG['authenticator_realm']})
