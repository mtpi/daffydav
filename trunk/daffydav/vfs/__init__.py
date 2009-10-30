#!/usr/bin/env python
# encoding: utf-8
"""
Virtual File System backends

Created by Matteo Pillon on 2009-07-26.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from fs.base import FSError
from webob import exc
from daffydav.lib.registry import authenticator, vfs

def check_if_forbidden(path, raise_error=True):
    """Raise an HTTPForbidden if there's any exception accessing file/dir"""
    # check if there are any exception
    try:
        if vfs.isdir(path):
            vfs.listdir(path)
        else:
            vfs.open(path).close()
    except FSError, e:
        if raise_error:
            ##FIXME: explanation too verbose?
            raise exc.HTTPForbidden(explanation=str(e))
        else:
            return True
    else:
        return False

def path_join(path, other_path):
    if path[-1]=='/' or other_path[0]=='/':
        return path+other_path
    else:
        return path+'/'+other_path

def isdir_alone(path):
    """
    Returns true when path is a directory without subdirectories
    """
    if check_if_forbidden(path, raise_error=False):
        return True
    child_dirs = [elem for elem in vfs.listdir(path) if vfs.isdir(path_join(path, elem))]
    if len(child_dirs) > 0:
        return False
    else:
        return True

class VFSImpersonationWrapper(object):
    """
    This wrapper incapsultates any vfs object in order to impersonate
    the logged-in user before any method call
    """
    
    def __init__(self, vfs):
        """
        VFSImpersonationWrapper(vfs)
         vfs: any vfs instance
         authenticator: any daffydav.authenticators.Authenticator instance
        """
        self.vfs = vfs
    
    def __getattr__(self, name):
        ##FIXME: assumed all vfs attributes used in the code are methods
        def wrapper(*args, **kwargs):
            function = getattr(self.vfs, name)
            return authenticator.run_as_current_user(function, *args, **kwargs)
        return wrapper
