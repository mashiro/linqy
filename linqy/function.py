#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
from linqy.utils import Undefined, identity

class Function(object):
    ''' function wrapper '''

    def __init__(self, func):
        if isinstance(func, Function):
            self.is_none = func.is_none
            self.func = func
            self.index = 0
            self.spec = func.spec
            self.arity = func.arity
        else:
            if func is None or func is Undefined:
                self.is_none = True
                self.func = identity
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

    __nonzero__ = __bool__

    def __call__(self, *args, **kwargs):
        if self.spec[1] is None: # has varargs
            if len(args) > self.arity:
                message = 'operation expected at most %d or %d (with index) arguments, demand %d' % (len(args), len(args) + 1, self.arity)
                raise TypeError(message)

        args += (self.index,)
        self.index += 1
        return self.func(*args[:self.arity], **kwargs)

class Not(Function):
    def __call__(self, *args, **kwargs):
        return not Function.__call__(self, *args, **kwargs)

