#!/usr/bin/env python
# encoding: utf-8
"""
copy.py

Created by Matteo Pillon on 2009-07-30.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from webob import exc
from daffydav.vfs import FSError

from daffydav.lib.registry import vfs, request

class COPY_MOVE:    
    def __init__(self, copy_or_move):
        source = request.path_info
        destination = request.headers.get('Destination')
        depth = request.headers.get('Depth', 'infinity')
        overwrite = request.headers.get('Overwrite')
        if not destination:
            raise exc.HTTPBadRequest(expnalantion='Missing Destination header')
        if request.body:
            raise exc.HTTPUnsupportedMediaType(explanation='COPY request must NOT provide an XML body.')
        
        self.source = source
        self.destination = destination
        self.copy_or_move = copy_or_move
        
        if vfs.isdir(self.path):
            self.depth = depth
        else:
            self.depth = '0'
        
        if self.depth!='0' and self.depth!='infinity':
            raise exc.HTTPBadRequest(explanation='Bad Depth specification (%s)' %(self.depth))
        
        if overwrite == 'T':
            self.overwrite = True
        else:
            self.overwrite = False
        
        basepath = re.sub(r'/[^/]+/?$', '', destination)
        if not vfs.exists(basepath):
            raise exc.HTTPConflict(explanation='Creation of a resource without an appropriately scoped parent collection.')
    
    def __call__(self):
        if vfs.exists(self.destination):
            if not self.overwrite:
                raise exc.HTTPPreconditionFailed(explanation='The destination URL is already mapped to a resource and Overwrite is F.')
            else:
                if vfs.isdir(self.destination):
                    vfs.removedir(self.destination, recursive=True)
                else:
                    vfs.remove(self.destination)
        ##FIXME: no Insufficient Storage notification
        if vfs.isdir(self.source):
            ##TODO: check for recursion (/A -> /A/B) or same resource (/A -> /A)
            #if ??RECURSION??:
            #    raise exc.HTTPForbidden(explanation='No recursion allowed.')
            if self.depth == 'infinity':
                try:
                    if self.copy_or_move == 'copy':
                        vfs.copydir(self.source, self.destination)
                    elif self.copy_or_move == 'move':
                        vfs.movedir(self.source, self.destination)
                except FSError, e:
                    ##FIXME: explanation too verbose?
                    raise exc.HTTPForbidden(explanation=str(e))
            elif self.depth == '0':
                raise exc.HTTPBadRequest(explanation='A depth of 0 is not implemented for collections.')
        else:
            try:
                if self.copy_or_move == 'copy':
                    vfs.copy(self.source, self.destination, overwrite=self.overwrite)
                elif self.copy_or_move == 'move':
                    vfs.move(self.source, self.destination)
            except FSError, e:
                ##FIXME: explanation too verbose?
                raise exc.HTTPForbidden(explanation=str(e))
        return exc.HTTPCreated(explanation='Successful copy.')
