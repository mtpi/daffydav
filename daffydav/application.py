import cgi, logging, sys
from paste.deploy import CONFIG
from webob import Request, Response, exc
from datetime import datetime
from webob import exc
from daffydav import filemanager, dav
from daffydav.vfs import VFSImpersonationWrapper

from daffydav.lib.registry import request, vfs, c, AttribSafeContextObj, authenticator

log = logging.getLogger(__name__)

def getVFS():
    """
    Return vfs object
    """
    VFS = CONFIG['vfs']
    real_vfs = VFS(authenticator.get_home_dir(), **CONFIG['vfs_options'])
    # wrap with impersonation object to get real user file permissions
    return VFSImpersonationWrapper(real_vfs)

def application(environ, start_response):
    """
    Main WSGI application
    """
    try:
        # thread-local objects
        environ['paste.registry'].register(request, Request(environ))
        environ['paste.registry'].register(vfs, getVFS())
        environ['paste.registry'].register(c, AttribSafeContextObj())
        
        # call filemanager resources server application if path starts with the right uri
        if request.path_info.startswith(CONFIG['filemanager_backend'].resources_uri):
            return CONFIG['filemanager_backend'].resources_app(environ, start_response)
        
        # check if requested method is allowed
        if request.method.upper() not in HTTPMethods._enumerate():
            # method not allowed, raise an exception and send allowed methods
            raise exc.HTTPMethodNotAllowed(headers={'Allow': HTTPMethods._allowed()}).exception
        method = eval('HTTPMethods.' + request.method.upper())
        response = method()
    
    except exc.HTTPException, e:
        # The exception object itself is a WSGI application/response
        response = e
    
    return response(environ, start_response)


class HTTPMethods:
    """
    This is the heart of the application.
    Here start all the requests and get routed to the right module (filemanager or dav)
    """
    
    @staticmethod
    def _enumerate():
        "Returns a list with allowed methods"
        return [elem for elem in HTTPMethods.__dict__.keys() if not elem.startswith('_')]
    
    @staticmethod
    def _allowed():
        """
        Returns a string with allowed methods, comma separated
        Example:
            OPTIONS,GET,HEAD,POST,DELETE,TRACE,PROPFIND,PROPPATCH,COPY,MOVE,LOCK,UNLOCK
        """
        allow = ''
        for method in HTTPMethods._enumerate():
            allow += method + ','
        return allow[:-1]
    
    @staticmethod
    def GET():
        return filemanager.serve_page()
    
    @staticmethod
    def HEAD():
        ##TODO: implement HEAD
        return HTTPMethods.GET()
    
    @staticmethod
    def POST():
        return HTTPMethods.GET()
    
    @staticmethod
    def OPTIONS():
        resp = HTTPMethods.HEAD()
        resp.headers['DAV'] = dav.__DAVClass__
        resp.headers['Allow'] = HTTPMethods._allowed()
        return resp
    
    @staticmethod
    def PROPFIND():
        propfind = dav.PROPFIND()
        return propfind()
    
    @staticmethod
    def MKCOL():
        mkcol = dav.MKCOL()
        return mkcol()
    
    @staticmethod
    def DELETE():
        delete = dav.DELETE()
        return delete()
    
    @staticmethod
    def PUT():
        put = dav.PUT()
        return put()
    
    @staticmethod
    def COPY():
        copy = dav.COPY_MOVE('copy')
        return copy()
    
    @staticmethod
    def MOVE():
        move = dav.COPY_MOVE('move')
        return move()

    @staticmethod
    def LOCK():
        lock = dav.LOCK()
        return lock()
    
    @staticmethod
    def UNLOCK():
        unlock = dav.UNLOCK()
        return unlock()
    
    @staticmethod
    def PROPPATCH():
        proppatch = dav.PROPPATCH()
        return proppatch()
