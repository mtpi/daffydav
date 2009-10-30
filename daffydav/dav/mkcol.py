#!/usr/bin/env python
# encoding: utf-8
"""
mkcol.py

Created by Matteo Pillon on 2009-07-30.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from webob import exc
from daffydav.vfs import FSError
import re

from daffydav.lib.registry import vfs, request

class MKCOL:
    def __init__(self):
        path = request.path_info
        if request.body:
            raise exc.HTTPUnsupportedMediaType(explanation='MKCOL request must NOT provide an XML body.')
        
        self.path = path
        
        if vfs.exists(self.path):
            raise exc.HTTPMethodNotAllowed(explanation='MKCOL can only be executed on an unmapped URL.')
        
        basepath = re.sub(r'/[^/]+/?$', '', path)
        if not vfs.exists(basepath):
            raise exc.HTTPConflict(explanation='A collection cannot be made at the Request-URI until one or more intermediate collections have been created.')
    
    def __call__(self):
        ##FIXME: no Insufficient Storage notification
        try:
            vfs.makedir(self.path)
        except FSError, e:
            ##FIXME: explanation too verbose?
            raise exc.HTTPForbidden(explanation=str(e))
        return exc.HTTPCreated(explanation='The collection was created.')
