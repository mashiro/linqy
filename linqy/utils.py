#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import itertools
import inspect
import types

def anonymouse(**kwargs):
    ''' make anonymouse type instance. '''
    return type('', (object,), kwargs)()

# Undefeiend value.
Undefined = anonymouse()

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
    ''' always retrun [value] '''
    def inner(*args, **kwargs):
        return value
    return inner

def identity(value):
    ''' return identity value '''
    return value

def next(iterator, default=Undefined):
    ''' return the next item from the iterator. '''
    iterate = getattr(iterator, 'next', None)
    if iterate is None:
        iterate = getattr(iterator, '__next__', None)
        if iterate is None:
            name = type(iterator).__name__
            raise TypeError('%s object is not an iterator' % name)

    if default == Undefined:
        return iterate()
    else:
        try:
            return iterate()
        except StopIteration:
            return default

def isgenerator(object):
    return isinstance(object, types.GeneratorType)


def isgeneratorfunction(object):
    ''' Return true if the object is a user-defined generator function. '''
    CO_GENERATOR = 0x20
    return ((inspect.isfunction(object) or inspect.ismethod(object)) and
            object.func_code.co_flags & CO_GENERATOR)

def issequence(object):
    ''' Return true if the object is a generator. '''
    return hasattr(object, '__len__') and hasattr(object, '__getitem__')

def tosequence(iterable):
    if issequence(iterable):
        return iterable
    else:
        return list(iterable)

def findattr(*candidates):
    ''' find a attribute in module or dict. '''

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
irange = findattr((__builtins__, 'xrange'), (__builtins__, 'range'))

