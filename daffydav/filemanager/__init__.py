#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Matteo Pillon on 2009-07-26.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from webob import exc
from daffydav.vfs import check_if_forbidden
from paste.deploy import CONFIG
from daffydav.lib.registry import vfs, request

import logging
log = logging.getLogger(__name__)

def serve_page():
    path = request.path_info
    action = request.GET.get('action')
    
    if not vfs.exists(path):
        raise exc.HTTPNotFound()
    
    check_if_forbidden(path)
    
    # action is not defined? use defaults...
    if not action:
        if vfs.isdir(path):
            action = 'listdir'
        else:
            action = 'view'
    
    return CONFIG['filemanager_backend'].run_action(action)
