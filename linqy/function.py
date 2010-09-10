#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import types

class Function(object):
    def __init__(self, func):
        if func is None:
            func = lambda x: x # identity
            self.is_none = True
        else:
            self.is_none = False
        self.index = 0
        self.func = func
        self.spec = inspect.getargspec(func)
        self.arity = len(self.spec[0])
        if type(func) is types.MethodType:
            self.arity -= 1 # remove self or cls

    def __bool__(self):
        return not self.is_none

    def __nonzero__(self):
        return self.__bool__()

    def __call__(self, *args, **kwargs):
        args += (self.index,)
        self.index += 1
        return self.func(*args[:self.arity], **kwargs)

