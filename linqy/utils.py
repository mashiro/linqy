#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import types
from linqy import compatible

def anonymous(**kwargs):
    ''' make anonymouse type instance. '''
    return type('', (object,), kwargs)()


def not_(func):
    @compatible.wraps(func)
    def inner(*args, **kwargs):
        return not func(*args, **kwargs)
    return inner

def always(value):
    ''' always retrun [value] '''
    def inner(*args, **kwargs):
        return value
    return inner

def identity(*args):
    ''' return identity value '''
    if len(args) == 1:
        return args[0]
    else:
        return args

def isgenerator(object):
    ''' return true if the object is a generator. '''
    return isinstance(object, types.GeneratorType)

def isgeneratorfunction(object):
    ''' return true if the object is a user-defined generator function. '''
    CO_GENERATOR = 0x20
    return ((inspect.isfunction(object) or inspect.ismethod(object)) and
            object.func_code.co_flags & CO_GENERATOR)

def issequence(object):
    ''' return true if the object is a sequence. '''
    return hasattr(object, '__len__') and hasattr(object, '__getitem__')

def tosequence(iterable):
    if issequence(iterable):
        return iterable
    else:
        return list(iterable)

