#!/usr/bin/env python
# encoding: utf-8
"""
delete.py

Created by Matteo Pillon on 2009-07-30.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from daffydav.vfs import FSError
from webob import exc

from daffydav.lib.registry import vfs, request

class DELETE:
    def __init__(self):
        path = request.path_info
        depth = request.headers.get('Depth', 'infinity')
        if request.body:
            raise exc.HTTPUnsupportedMediaType(explanation='DELETE request must NOT provide an XML body.')
        
        self.path = path
        self.depth = depth
        
        if not vfs.exists(self.path):
            raise exc.HTTPNotFound()
    
    def __call__(self):
        try:
            if vfs.isdir(self.path):
                if self.depth == 'infinity':
                    recursive=True
                else:
                    recursive=False
                vfs.removedir(self.path, recursive=recursive)
            else:
                vfs.remove(self.path)
        except FSError, e:
            ##FIXME: explanation too verbose?
            raise exc.HTTPForbidden(explanation=str(e))
        return exc.HTTPOk(explanation='Resource deleted')
