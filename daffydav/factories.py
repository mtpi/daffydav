#!/usr/bin/env python
# encoding: utf-8
"""
factories.py

Created by Matteo Pillon on 2009-08-20.
Copyright (c) 2009 Matteo Pillon. All rights reserved.
"""

# daffydav main application
from daffydav.application import application

#utility functions
from paste.util.import_string import eval_import
from daffydav.lib.config import ConfigBackendOptions
from ConfigParser import SafeConfigParser
import os.path

#middleware
from paste.deploy.config import ConfigMiddleware
from paste.auth.basic import AuthBasicHandler
from paste.registry import RegistryManager

#daemons
from daffydav.authenticators import AuthDaemon
from daffydav.dav.locking import LockingDaemon

import logging
log = logging.getLogger(__name__)

def config_factory(args):
    """
    for spawning support
     spawn -f daffydav.factories.config_factory daffydav.conf
    """
    args['app_factory'] = 'daffydav.factories.make_app'
    args['config_file'] = args['args'][0]
    return args

def make_app(global_conf, **kw):
    
    CONFIG = global_conf.copy()
    CONFIG.update(kw)
    
    # load daffydav.conf
    daffydav_conf = SafeConfigParser()
    daffydav_conf.read(CONFIG['config_file'])
    
    # authenticator backend
    auth = eval_import(daffydav_conf.get('authenticator', 'backend'))
    auth_options = ConfigBackendOptions(daffydav_conf.items('authenticator'))
    CONFIG['authenticator_realm'] = auth_realm = daffydav_conf.get('authenticator', 'realm')
    auth_daemon = AuthDaemon(auth, auth_options)
    
    # virtual filesystem backend
    CONFIG['vfs'] = eval_import(daffydav_conf.get('vfs', 'backend'))
    CONFIG['vfs_options'] = ConfigBackendOptions(daffydav_conf.items('vfs'))
    
    # filemanager interface backend
    fmbackend = eval_import(daffydav_conf.get('filemanager', 'backend'))
    fmbackend_options = ConfigBackendOptions(daffydav_conf.items('filemanager'))
    CONFIG['filemanager_backend'] = fmbackend(**fmbackend_options)
    
    # === MIDDLEWARE ===
    # Main application
    app = application
    # Authenticator Middleware
    app = AuthBasicHandler(app, auth_realm, auth_daemon.authfunc)
    # paste RegistryManager middleware for thread-local objects
    app = RegistryManager(app)
    # ConfigMiddleware means that paste.deploy.CONFIG will,
    # during this request (threadsafe) represent the
    # configuration dictionary we set up:
    app = ConfigMiddleware(app, CONFIG)
    
    return app
