#!/usr/bin/env python
# -*- coding: utf-8 -*-
from linqy.utils import not_

class Comparison(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __eq__(self, other):
        return self.wrapped == self.wrappedvalue(other)

    def __ne__(self, other):
        return self.wrapped != self.wrappedvalue(other)

    def __lt__(self, other):
        return self.wrapped < self.wrappedvalue(other)

    def __le__(self, other):
        return self.wrapped <= self.wrappedvalue(other)

    def __gt__(self, other):
        return self.wrapped > self.wrappedvalue(other)

    def __ge__(self, other):
        return self.wrapped >= self.wrappedvalue(other)

    @classmethod
    def wrappedvalue(cls, value):
        if isinstance(value, Comparison):
            return cls.wrappedvalue(value.wrapped)
        return value

class Reverse(Comparison):
    __lt__ = not_(Comparison.__lt__)
    __le__ = not_(Comparison.__le__)
    __gt__ = not_(Comparison.__gt__)
    __ge__ = not_(Comparison.__ge__)

