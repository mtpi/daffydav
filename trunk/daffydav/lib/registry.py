#!/usr/bin/env python
# encoding: utf-8
"""
registry.py

All the code here is taken from Pylons! :)
"""

from paste.registry import StackedObjectProxy

request = StackedObjectProxy(name="request")
tmpl_context = c = StackedObjectProxy(name="tmpl_context or C")
vfs = StackedObjectProxy(name="vfs")
authenticator = StackedObjectProxy(name="authenticator")

class ContextObj(object):
    """The :term:`tmpl_context` object, with strict attribute access
    (raises an Exception when the attribute does not exist)"""
    def __repr__(self):
        attrs = [(name, value)
                 for name, value in self.__dict__.items()
                 if not name.startswith('_')]
        attrs.sort()
        parts = []
        for name, value in attrs:
            value_repr = repr(value)
            if len(value_repr) > 70:
                value_repr = value_repr[:60] + '...' + value_repr[-5:]
            parts.append(' %s=%s' % (name, value_repr))
        return '<%s.%s at %s%s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self)),
            ','.join(parts))


class AttribSafeContextObj(ContextObj):
    """The :term:`tmpl_context` object, with lax attribute access (
    returns '' when the attribute does not exist)"""
    def __getattr__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            pylons_log.debug("No attribute called %s found on c object, "
                             "returning empty string", name)
            return ''
