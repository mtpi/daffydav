#!/usr/bin/env python
# encoding: utf-8
"""
config.py

Created by Matteo Pillon on 2009-07-26.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

class ConfigBackendOptions(dict):
    """
    kwargs = ConfigBackendOptions(config.items('section'), startswith='backend.')
    
    returns a dict with options in the specified config section ([(k,v), ...])
    """
    def __init__(self, config_items, startswith='backend.'):
        if not startswith[-1]=='.':
            startswith+='.'
        for k,v in config_items:
            if k.startswith(startswith):
                self[k.replace(startswith, '')]=v
