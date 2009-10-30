#!/usr/bin/env python
# encoding: utf-8
"""
lock.py

Created by Matteo Pillon on 2009-07-30.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from webob import exc
import uuid

from daffydav.lib.registry import vfs, request

# TODO: work in progress...

class Lock(object):
    def __init__(self, path, ltype='write', scope='exclusive', depth='infinity', timeout=None, owner=None):
        self.path = path
        self.type = ltype
        self.scope = scope
        self.depth = depth
        self.timeout = timeout
        self._gen_token()
    
    def _gen_token(self):
        self.token = uuid.uuid4()

class LockingDaemon(object):
    """
    LockingDaemon
    
    Provides locking facilities
    """
    ##FIXME: add filebased (for persistency) locking database
    
    def __init__(self):
        self.engaged_locks = []

class LOCK:
    def __init__(self):
        path = request.path_info
        
    def __call__(self):
        return exc.HTTPOk(explanation='Locked.')

class UNLOCK:
    def __init__(self):
        path = request.path_info
        
    def __call__(self):
        return exc.HTTPOk(explanation='UnLocked.')
