#!/usr/bin/env python
# -*- coding: utf-8 -*-
from linqy.undefined import Undefined, isundefined

class AttributeNotFoundError(Exception):
    pass

def _findattr(*candidates):
    for candidate in candidates:
        if isinstance(candidate, tuple):
            module, name = candidate
            if isinstance(module, dict):
                if name in module:
                    return module[name]
            else:
                if isinstance(module, str):
                    try:
                        module = __import__(module)
                    except ImportError:
                        continue
                if hasattr(module, name):
                    return getattr(module, name)
        else:
            return candidate

    raise AttributeNotFoundError(candidates)

imap = _findattr(('itertools', 'imap'), (__builtins__, 'map'))
izip = _findattr(('itertools', 'izip'), (__builtins__, 'zip'))
ifilter = _findattr(('itertools', 'ifilter'), (__builtins__, 'filter'))
ifilterfalse = _findattr(('itertools', 'ifilterfalse'), ('itertools', 'filterfalse'))
irange = _findattr((__builtins__, 'xrange'), (__builtins__, 'range'))
basestring = _findattr((__builtins__, 'basestring'), (__builtins__, 'str'))

def next(iterator, default=Undefined()):
    ''' return the next item from the iterator. '''
    iterate = getattr(iterator, 'next', None)
    if iterate is None:
        iterate = getattr(iterator, '__next__', None)
        if iterate is None:
            name = type(iterator).__name__
            raise TypeError('%s object is not an iterator' % name)
    if isundefined(default):
        return iterate()
    else:
        try:
            return iterate()
        except StopIteration:
            return default

wraps = _findattr(('functools', 'wraps'), None)
if wraps is None:
    def wraps(wrapped):
        ''' functools.wraps for Python2.4 '''
        def inner(wrapper):
            wrapper.__module__ = wrapped.__module__
            wrapper.__name__ = wrapped.__name__
            wrapper.__doc__ = wrapped.__doc__
            wrapper.__dict__.update(wrapped.__dict__)
            return wrapper
        return inner

