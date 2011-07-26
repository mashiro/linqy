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

    def __init__(self, wrapped=None, arity=None):
        self.arity = arity

        if wrapped is None or wrapped is _undefined:
            # identity
            self.func = utils.identity
            self.func_arity = self.arity
            self.index = None
        elif isinstance(wrapped, Function):
            # function object
            self.func = wrapped.func
            self.func_arity = wrapped.func_arity
            if wrapped.index is None:
                self.index = None
            else:
                self.index = 0
        elif isinstance(wrapped, compatible.basestring):
            # string evaluator
            self.func = Evaluator(wrapped)
            self.func_arity = None
            self.index = 0
        elif inspect.isbuiltin(wrapped) or inspect.ismethoddescriptor(wrapped):
            # built-in function
            self.func = wrapped
            self.func_arity = None
            self.index = None
        else:
            # user defined function
            self.func = wrapped

            spec = inspect.getargspec(wrapped)
            args = spec[0]
            varargs = spec[1]

            if varargs is not None:
                self.func_arity = None
                self.index = 0
            else:
                self.func_arity = len(args)
                if inspect.ismethod(wrapped):
                    self.func_arity -= 1 # reject self or cls

                if self.arity is not None and self.arity < self.func_arity:
                    self.index = 0
                else:
                    self.index = None

    def __bool__(self):
        return not self.func is utils.identity

    __nonzero__ = __bool__

    def __call__(self, *args, **kwargs):
        if self.index is not None:
            args += (self.index,)

        if self.func_arity is not None and self.func_arity != len(args):
            raise TypeError('operation expected at most %d arguments, demand %d' % (len(args), self.func_arity))

        result = self.func(*args, **kwargs)

        if self.index is not None:
            self.index += 1

        return result



def Q(source, globals=None, locals=None):
    if globals is None or locals is None:
        frame = inspect.stack()[1][0]
        globals = globals or frame.f_globals
        locals = locals or frame.f_locals
    return Evaluator(source, globals=globals, locals=locals)

