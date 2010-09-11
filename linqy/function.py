#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect

class Function(object):
    def __init__(self, func):
        if isinstance(func, Function):
            self.is_none = func.is_none
            self.func = func
            self.index = 0
            self.spec = func.spec
            self.arity = func.arity
        else:
            if func is None:
                self.is_none = True
                self.func = lambda x: x # identity
            else:
                self.is_none = False
                self.func = func
            self.index = 0
            self.spec = inspect.getargspec(self.func)
            self.arity = len(self.spec[0])
            if inspect.ismethod(self.func):
                self.arity -= 1 # remove self or cls

    def __bool__(self):
        return not self.is_none

    def __nonzero__(self):
        return self.__bool__()

    def __call__(self, *args, **kwargs):
        args += (self.index,)
        self.index += 1
        return self.func(*args[:self.arity], **kwargs)

class Not(Function):
    def __call__(self, *args, **kwargs):
        return not Function.__call__(self, *args, **kwargs)

