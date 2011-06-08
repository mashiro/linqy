#!/usr/bin/env python
# -*- coding: utf-8 -*-
from linqy.undefined import _undefined

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
min = _findattr((__builtins__, 'min'))
max = _findattr((__builtins__, 'max'))
sum = _findattr((__builtins__, 'sum'))
reduce = _findattr((__builtins__, 'reduce'), ('functools', 'reduce'))

def next(iterator, default=_undefined):
    ''' return the next item from the iterator. '''
    iterate = getattr(iterator, 'next', None)
    if iterate is None:
        iterate = getattr(iterator, '__next__', None)
        if iterate is None:
            name = type(iterator).__name__
            raise TypeError('%s object is not an iterator' % name)
    if default is _undefined:
        return iterate()
    else:
        try:
            return iterate()
        except StopIteration:
            return default

izip_longest = _findattr(('itertools', 'izip_longest'), ('itertools', 'zip_longest'), None)
if izip_longest is None:
    import itertools
    def izip_longest(fillvalue=_undefined, *args):
        def sentinel(counter = ([fillvalue]*(len(args)-1)).pop):
            yield counter() # yields the fillvalue, or raises IndexError
        fillers = itertools.repeat(fillvalue)
        iterators = [itertools.chain(iterator, sentinel(), fillers) for iterator in args]
        try:
            for tup in izip(*iters):
                yield tup
        except IndexError:
            pass

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

