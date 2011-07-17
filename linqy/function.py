#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
from linqy import compatible
from linqy.undefined import _undefined
from linqy import utils

__placeholders__ = [
    ['_1', '_'],
    ['_2'],
    ['_3'],
    ['_4'],
    ['_5']
]

class Evaluator(object):
    ''' string evaluation wrapper '''

    def __init__(self, source, globals=None, locals=None):
        self.code = compile(source, '<string>', 'eval')
        self.globals = (globals or {}).copy()
        self.locals = (locals or {}).copy()

    def __call__(self, *args, **kwargs):
        # setup placeholders
        self.locals.update(kwargs)
        for i, arg in enumerate(args[:len(__placeholders__)]):
             for placeholder in __placeholders__[i]:
                 self.locals[placeholder] = arg

        # evaluation
        return eval(self.code, self.globals, self.locals)


class Function(object):
    ''' function wrapper '''

    def __init__(self, func, arity=None):
        self.arity = arity
        self.index = None

        if isinstance(func, Function):
            # Function object
            self.is_none = func.is_none
            self.func = func
            self.spec = func.spec
            if arity is None:
                self.arity = func.arity
            self.with_index = func.with_index
        elif isinstance(func, compatible.basestring):
            # string eval
            self.is_none = False
            self.func = Evaluator(func)
            self.spec = None
            self.with_index = True
        elif func is None or func is _undefined:
            # identity function
            self.is_none = True
            self.func = utils.identity
            self.spec = inspect.getargspec(self.func)
            self.with_index = False
        else:
            # user function
            self.is_none = False
            self.func = func
            self.spec = inspect.getargspec(self.func)

            func_arity = len(self.spec[0])
            if inspect.ismethod(self.func):
                func_arity -= 1
            if self.arity is None:
                self.arity = func_arity
            self.with_index = self.arity < func_arity

        if self.with_index:
            self.index = 0

    def __bool__(self):
        return not self.is_none

    __nonzero__ = __bool__

    def __call__(self, *args, **kwargs):
        if self.arity or self.spec and self.spec[0] is None: # varargs is None
            if self.arity != len(args):
                message = 'operation expected at most %d or %d (with index) arguments, demand %d' % (len(args), len(args) + 1, self.arity)
                raise TypeError(message)

        if self.with_index:
            args += (self.index,)
            self.index += 1

        return self.func(*args, **kwargs)


def Q(source, globals=None, locals=None):
    if globals is None or locals is None:
        frame = inspect.stack()[1][0]
        globals = globals or frame.f_globals
        locals = locals or frame.f_locals
    return Evaluator(source, globals=globals, locals=locals)

