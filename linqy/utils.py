#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import itertools

def anonymouse(**kwargs):
    ''' make anonymouse type instance. '''
    return type('', (object,), kwargs)()

# nil value
nil = anonymouse()

def wraps(wrapped):
    ''' functools.wraps for Python2.4 '''
    def inner(wrapper):
        wrapper.__module__ = wrapped.__module__
        wrapper.__name__ = wrapped.__name__
        wrapper.__doc__ = wrapped.__doc__
        wrapper.__dict__.update(wrapped.__dict__)
        return wrapper
    return inner

def not_(func):
    @wraps(func)
    def inner(*args, **kwargs):
        return not func(*args, **kwargs)
    return inner

def always(value):
    def inner(*args, **kwargs):
        return value
    return inner

def next(iterator, default=nil):
    ''' return the next item from the iterator. '''
    f = getattr(iterator, 'next', None)
    if f is None:
        f = getattr(iterator, '__next__')

    if default == nil:
        return f()
    else:
        try:
            return f()
        except StopIteration:
            return default

def issequence(object):
    return hasattr(object, '__len__') and hasattr(object, '__getitem__')

def tosequence(iterable):
    if issequence(iterable):
        return iterable
    else:
        return list(iterable)

def findattr(*candidates):
    ''' find a attribute in module or dict '''

    class AttributeNotFoundError(Exception):
        pass

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

# compatible python2.x,3.x
imap = findattr((itertools, 'imap'), (__builtins__, 'map'))
izip = findattr((itertools, 'izip'), (__builtins__, 'zip'))
ifilter = findattr((itertools, 'ifilter'), (__builtins__, 'filter'))
ifilterfalse = findattr((itertools, 'ifilterfalse'), (itertools, 'filterfalse'))
irange = findattr((__builtins__, 'xrange'), range)
basestring = findattr((__builtins__, 'basestring'), (__builtins__, 'str'))

