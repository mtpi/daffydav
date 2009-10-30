#!/usr/bin/env python
# encoding: utf-8
"""
actions.py

Created by Matteo Pillon on 2009-07-27.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from webob import Response, exc
import mimetypes
import simplejson as json
from xml.etree import ElementTree as ET
from daffydav.vfs import path_join, isdir_alone
from daffydav.lib.registry import vfs, request, c, authenticator
from daffydav.lib.templating import render
from daffydav.filemanager import helpers

import logging
log = logging.getLogger(__name__)

__all__ = ['view', 'listdir', 'logout', 'navigator', 'contents']

def view():
    """
    Serve file content as is
    """
    ## FIXME: use file_wrapper
    path = request.path_info
    resp = Response(vfs.getcontents(path))
    (content_type, resp.content_encoding) = mimetypes.guess_type(path)
    if content_type:
        resp.content_type = content_type
    else:
        resp.content_type = 'application/octet-stream'
    return resp

def listdir():
    return render('/main.mako')

def logout():
    authenticator.logout(request.GET.get('username'))
    return exc.HTTPMovedPermanently(location='/')

def navigator():
    open_folders = json.loads(request.POST.get('open_folders', '[]'))
    # filer DirectoryAlone folders
    open_folders = [folder for folder in open_folders if not isdir_alone(folder)]
    log.debug('open_folders: ' + repr(open_folders))
    xml_tree = ET.TreeBuilder()
    xml_tree.start('span', {})
    helpers.folder_div(request.path_info, xml_tree, open_folders=open_folders)
    xml_tree.end('span')
    xml = xml_tree.close()
    resp = Response(ET.tostring(xml, encoding='utf-8').replace('&apos;', "'"))
    resp.content_type = 'text/html'
    resp.content_encoding = 'utf-8'
    return resp

def contents():
    return render('/contents.mako')

