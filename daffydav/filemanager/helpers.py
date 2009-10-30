#!/usr/bin/env python
# encoding: utf-8
"""
helpers.py

Created by Matteo Pillon on 2009-08-19.
Copyright (c) 2009 Matteo Pillon. All rights reserved.

Contains various helpers for generating ajax replies
"""

from xml.etree import ElementTree as ET
from daffydav.lib.registry import vfs
from daffydav.vfs import path_join, isdir_alone

def folder_div(path, xml_tree, open_folders=[]):
    """
    Generate a <div class="folder">
    
     path: directory path
     parent: any parent tag to write contents to
     open_folders: a list of paths to show opened
    """
    
    ##FIXME: opening aloneFolders doesnt close the empty div
    
    for directory in [elem for elem in vfs.listdir(path) if vfs.isdir(path_join(path, elem))]:
        directoryFullPath = path_join(path, directory)
        directory_a_attrs = {'href': "javascript:openCloseDir('"+directoryFullPath+"')"}
        if directoryFullPath in open_folders:
            directory_a_attrs['class'] = 'openFolder'
        elif isdir_alone(directoryFullPath):
            directory_a_attrs['class'] = 'aloneFolder'
        else:
            directory_a_attrs['class'] = 'closedFolder'
        xml_tree.start('a', directory_a_attrs)
        xml_tree.data(directory)
        xml_tree.end('a')
        
        xml_tree.start('br', {})
        xml_tree.end('br')
        
        if directoryFullPath in open_folders:
            xml_tree.start('div', {'class': 'folder'})
            folder_div(directoryFullPath, xml_tree, open_folders=open_folders)
            xml_tree.end('div')
