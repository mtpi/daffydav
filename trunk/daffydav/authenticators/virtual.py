#!/usr/bin/env python
# encoding: utf-8
"""
virtual.py

Created by Matteo Pillon on 2009-08-18.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

import logging
log = logging.getLogger(__name__)

class VirtualAuthenticator():
    """
    VirtualAuthenticator
    
    Authenticate virtual users
    """
    
    virtual = True
    
    def _validate(self):
        ##TODO: not implemented
        return False
