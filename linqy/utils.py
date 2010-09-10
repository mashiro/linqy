#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import itertools

class AttributeNotFoundError(Exception):
    pass

def findattr(*candidates):
    ''' find a attribute in module or dict '''
    for candidate in candidates:
        if isinstance(candidate, tuple):
            module, name = candidate
            if isinstance(module, dict):
                if name in module:
                    return module[name]
            else:
                if hasattr(module, name):
                    return getattr(module, name)
        else:
            return candidate
    raise AttributeNotFoundError

imap = findattr((itertools, 'imap'), (__builtins__, 'map'))
izip = findattr((itertools, 'izip'), (__builtins__, 'zip'))
ifilter = findattr((itertools, 'ifilter'), (__builtins__, 'filter'))
ifilterfalse = findattr((itertools, 'ifilterfalse'), (itertools, 'filterfalse'))
irange = findattr((__builtins__, 'xrange'), range)
next = findattr((__builtins__, 'next'), lambda x: x.next())
basestring = findattr((__builtins__, 'basestring'), (__builtins__, 'str'))

# functools.wraps for Python2.4
def wraps(wrapped):
    def inner(wrapper):
        wrapper.__module__ = wrapped.__module__
        wrapper.__name__ = wrapped.__name__
        wrapper.__doc__ = wrapped.__doc__
        wrapper.__dict__.update(wrapped.__dict__)
        return wrapper
    return inner

def not_(func):
    def inner(*args, **kwargs):
        return not func(*args, **kwargs)
    return inner

def issequence(object):
    return hasattr(object, '__len__') and hasattr(object, '__getitem__')

def tosequence(iterable):
    if issequence(iterable):
        return iterable
    else:
        return list(iterable)

def anonymouse(**kwargs):
    ''' make anonymouse type instance '''
    return type('', (object,), kwargs)()

