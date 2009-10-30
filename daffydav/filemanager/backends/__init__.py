#!/usr/bin/env python
# encoding: utf-8
"""
FileManager Backends

Created by Matteo Pillon on 2009-08-21.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from daffydav.lib.registry import c, vfs
from webob import Response, exc

import logging
log = logging.getLogger(__name__)

class FileManagerBackend(object):
    
    resources_uri = '/_$daffydav_filemanager_resources/'
    
    def __init__(self):
        """
        init must provide
         self.templatelookup: Mako TemplateLookup instance
         self.real_resources_app: something like paste.fileapp.DirectoryApp for
           serving resources in <resources_uri>
         self.actions: a dictionary with actions and their function reference,
           like this: {'list': list, 'view': view, ...}
        """
        pass
    
    def resources_app(self, environ, start_response):
        """
        Serves filemanager backend resource files (pictures, javascripts, stylesheets, ...)
        
        This function patches path_info in the environ stripping resources_uri,
        then calls self.real_resources_app
        """
        environ['PATH_INFO']=environ['PATH_INFO'].replace(self.resources_uri, '/')
        log.debug('resources_app request for path: ' + environ['PATH_INFO'])
        return self.real_resources_app(environ, start_response)
    
    def run_action(self, action):
        """
        Any request like this: /path/?action=<action> calls this function
        Basic actions are:
         view: return file as-is
         listdir: directory listing
        """
        if action not in self.actions:
            raise exc.HTTPBadRequest('Invalid action: ' + action + '.')
        return self.actions[action]()
    
    def render(self, templatename):
        """
        return rendered template
        """
        template = self.templatelookup.get_template(templatename)
        return Response(template.render_unicode(c=c, vfs=vfs))

