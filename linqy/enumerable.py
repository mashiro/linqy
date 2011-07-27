#!/usr/bin/env python
# -*- coding: utf-8 -*-
from linqy import compatible
from linqy import utils

class Enumerable(object): # {{{1
    ''' enumerable object '''

    def __init__(self, generator):
        self._source = generator

    def __iter__(self):
        return self._source()

    @classmethod
    def __extend__(cls, name, func):
        if not hasattr(cls, '_operations'):
            cls._operations = {}
        cls._operations[name] = func
        setattr(cls, name, func)


class SequenceEnumerable(Enumerable): # {{{1
    ''' sequence enumerable object '''

    def __init__(self, iterable):
        Enumerable.__init__(self, utils.tosequence(iterable))

    def __iter__(self):
        return iter(self._source)

    def __len__(self):
        return self._source.__len__()

    def __getitem__(self, key):
        return self._source.__getitem__(key)

    def __contains__(self, item):
        return self._source.__contains__(item)


class OrderedEnumerable(Enumerable): # {{{1
    ''' ordered enumerable object '''

    def __init__(self, iterable, keys):
        Enumerable.__init__(self, iterable)
        self._keys = keys

    def __iter__(self):
        key = lambda x: list(map(lambda y: y(x), self._keys))
        return iter(sorted(self._source, key=key))


