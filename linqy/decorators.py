#!/usr/bin/env python
# -*- coding: utf-8 -*-
from linqy import compatible

def extensionmethod(type):
    def outer(func):
        @compatible.wraps(func)
        def inner(self, *args, **kwargs):
            if hasattr(self, '__extensionmethod__'):
                return self.__extensionmethod__(func, *args, **kwargs)
            else:
                return func(self, *args, **kwargs)
        if hasattr(type, '__extend__'):
            type.__extend__(func.__name__, inner)
        else:
            setattr(type, func.__name__, inner)
        return func
    return outer

def lazymethod(type):
    def outer(func):
        @compatible.wraps(func)
        def inner(*args, **kwargs):
            return type(lambda: func(*args, **kwargs))
        return inner
    return outer

