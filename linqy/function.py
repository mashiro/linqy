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
        for (i, arg) in enumerate(args[:len(__placeholders__)]):
             for placeholder in __placeholders__[i]:
                 self.locals[placeholder] = arg

        # evaluation
        return eval(self.code, self.globals, self.locals)


class Function(object):
    ''' function wrapper '''

    def __init__(self, func):
        self.index = 0
        if isinstance(func, Function):
            self.is_none = func.is_none
            self.func = func
            self.spec = func.spec
            self.arity = func.arity
        elif isinstance(func, compatible.basestring):
            self.is_none = False
            self.func = Evaluator(func)
            self.spec = None
            self.arity = len(__placeholders__)
        else:
            if func is None or func is _undefined:
                self.is_none = True
                self.func = utils.identity
            else:
                self.is_none = False
                self.func = func
            self.spec = inspect.getargspec(self.func)
            self.arity = len(self.spec[0])
            if inspect.ismethod(self.func):
                self.arity -= 1 # remove self or cls

    def __bool__(self):
        return not self.is_none

    __nonzero__ = __bool__

    def __call__(self, *args, **kwargs):
        if self.spec and self.spec[1] is None: # varargs is None
            if len(args) > self.arity:
                message = 'operation expected at most %d or %d (with index) arguments, demand %d' % (len(args), len(args) + 1, self.arity)
                raise TypeError(message)

        args += (self.index,)
        self.index += 1
        return self.func(*args[:self.arity], **kwargs)


def Q(source, globals=None, locals=None):
    if globals is None or locals is None:
        frame = inspect.stack()[1][0]
        globals = globals or frame.f_globals
        locals = locals or frame.f_locals
    return Evaluator(source, globals=globals, locals=locals)

