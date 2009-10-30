#!/usr/bin/env python
# encoding: utf-8
"""
propfind.py

Created by Matteo Pillon on 2009-07-28.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

from xml.etree import ElementTree as ET
ET._namespace_map['DAV:'] = 'D'
from webob import Response, exc
from daffydav.vfs import check_if_forbidden, path_join

from daffydav.lib.registry import vfs, request

import logging
log = logging.getLogger(__name__)


class PROPFIND:
    """
    PROPFIND HTTP/1.1 Method manager
    """
    
    # properties returned/supported for every resource
    ## TODO: only base properties implemented
    ALLPROPS = [
                '{DAV:}creationdate',
                ##FIXME:not implemented '{DAV:}displayname',
                ##FIXME:not implemented '{DAV:}getcontentlanguage'
                '{DAV:}getcontentlength',
                ##FIXME:not implemented '{DAV:}getcontenttype',
                ##FIXME:not implemented '{DAV:}getetag',
                ##FIXME:not implemented (LOCKING) '{DAV:}lockdiscovery',
                '{DAV:}getlastmodified',
                '{DAV:}resourcetype',
                ##FIXME:not implemented (LOCKING) '{DAV:}supportedlock',
                ]
    
    def __init__(self):
        "Save and check a PROPFIND request, must call the instance to generate response"
        
        self.path = request.path_info
        # check if it exists...
        if not vfs.exists(self.path):
            raise exc.HTTPNotFound()
        check_if_forbidden(self.path)
        
        body = request.body
        if not body:
            raise exc.HTTPUnsupportedMediaType(explanation='PROPFIND request must provide an XML body.')
        
        self.xmlreq = ET.fromstring(body)
        
        # check if depth is correct...
        depth = request.headers.get('Depth', 'infinity')
        if depth!='1' and depth!='0':
            raise exc.HTTPForbidden(explanation='PROPFIND only allows Depth of 0 or 1 (propfind-finite-depth).')
        else:
            self.depth = depth
        
        # if it's a file, depth must be 0
        if vfs.isfile(self.path):
            self.depth = '0'
    
    def __call__(self):
        "Generate the response"
        if self.xmlreq.find('{DAV:}prop'):
            # save only the tag of requested properties
            props = [prop.tag for prop in self.xmlreq.find('{DAV:}prop').getchildren()]
            resp_xml = self.gen_prop_tree(props)
        elif self.xmlreq.find('{DAV:}allprop') is not None:
            resp_xml = self.gen_prop_tree(self.ALLPROPS)
        elif self.xmlreq.find('{DAV:}propname') is not None:
            resp_xml = self.gen_prop_tree(self.ALLPROPS, only_names=True)
        else:
            raise exc.HTTPBadRequest(explanation='Unknown PROPFIND request body.')
        
        ## FIXME: fix unicode
        resp_body = '<?xml version="1.0" encoding="utf-8" ?>'
        resp_body += ET.tostring(resp_xml, encoding='utf-8')
        resp = Response(resp_body)
        resp.content_type = 'application/xml'
        resp.content_encoding = 'utf-8'
        resp.status_int = 207 #Multi Status
        return resp
    
    def gen_prop_tree(self, props, only_names=False):
        XMLroot = ET.Element('{DAV:}multistatus')
        XMLresp = ET.SubElement(XMLroot, '{DAV:}response')
        
        # depth==0: only this resource
        resources = [self.path]
        # depth==1: add resources of the collection
        if self.depth == '1':
            ##FIXME: fix unicode (most errors here!)
            resources.extend([path_join(self.path,res) for res in vfs.listdir(self.path)])
        
        for res in resources:
            XMLres_href = ET.SubElement(XMLresp, '{DAV:}href')
            XMLres_href.text = res
            XMLres_propstat = ET.SubElement(XMLresp, '{DAV:}propstat')
            XMLres_propstat_prop = ET.SubElement(XMLres_propstat, '{DAV:}prop')
            
            res_info = vfs.getinfo(res)
            if '{DAV:}creationdate' in props:
                prop = ET.SubElement(XMLres_propstat_prop, '{DAV:}creationdate')
                if not only_names:
                    prop.text = res_info['created_time'].strftime('%Y-%m-%dT%H:%M:%SZ')
            if '{DAV:}getcontentlength' in props:
                prop = ET.SubElement(XMLres_propstat_prop, '{DAV:}getcontentlength')
                if not only_names:
                    prop.text = str(res_info['size'])
            if '{DAV:}getlastmodified' in props:
                prop = ET.SubElement(XMLres_propstat_prop, '{DAV:}getlastmodified')
                if not only_names:
                    prop.text = res_info['modified_time'].strftime('%Y-%m-%dT%H:%M:%SZ')
            if '{DAV:}resourcetype' in props:
                restype = ET.SubElement(XMLres_propstat_prop, '{DAV:}resourcetype')
                if not only_names and vfs.isdir(res):
                    ET.SubElement(restype,'{DAV:}collection')
            ##FIXME: add DAV:supportedlock and DAV:lockdiscovery
            
            XMLres_propstat_status = ET.SubElement(XMLres_propstat, '{DAV:}status')
            XMLres_propstat_status.text = 'HTTP/1.1 200 OK'
            #XMLres_propstat_status = ET.SubElement(XMLres_propstat, '{DAV:}status')
            #XMLres_propstat_status.text = 'HTTP/1.1 403 Forbidden'
            #XMLres_propstat_responsedescription = ET.SubElement(XMLres_propstat, '{DAV:}responsedescription')
            #XMLres_propstat_responsedescription.text = 'There has been an access violation error.'
        return XMLroot

class PROPPATCH:
    ## TODO: PROPPATCH not implemented
    def __init__(self):
        self.path = request.path_info
        self.body = request.body
        if not self.body:
            raise exc.HTTPUnsupportedMediaType(explanation='PROPPATCH request must provide an XML body.')
        raise exc.HTTPForbidden(explanation='PROPPATCH not implemented on this server.')
