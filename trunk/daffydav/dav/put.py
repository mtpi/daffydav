#!/usr/bin/env python
# encoding: utf-8
"""
put.py

Created by Matteo Pillon on 2009-08-01.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from daffydav.vfs import FSError
from webob import exc
import re, logging

from daffydav.lib.registry import vfs, request

log = logging.getLogger(__name__)

BUFFER_SIZE = 4096

class PUT:
    def __init__(self):
        self.path = request.path_info
        depth = request.headers.get('Depth', 'infinity')
        
        if request.body:
            raise exc.HTTPUnsupportedMediaType(explanation='DELETE request must NOT provide an XML body.')
        
        if vfs.isdir(self.path):
            raise exc.HTTPMethodNotAllowed(explanation='URI refers to an existing collection.')
        
        basepath = re.sub(r'/[^/]+/?$', '', path)
        if not vfs.exists(basepath):
            raise exc.HTTPConflict(explanation='Creation of a resource without an appropriately scoped parent collection.')
        
        try:
            self.file = vfs.open(path, mode='w')
        except FSError, e:
            ##FIXME: explanation too verbose?
            raise exc.HTTPForbidden(explanation=str(e))
    
    def __call__(self):
        while True:
            ##FIXME: no Insufficient Storage notification
            buffer = request.body_file.read(BUFFER_SIZE)
            if not buffer:
                break
            self.file.write(buffer)
        
        self.file.close()
        return exc.HTTPOk(explanation='Data written.')
