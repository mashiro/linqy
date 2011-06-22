#!/usr/bin/env python
# -*- coding: utf-8 -*-
from linqy import compatible
from linqy import utils

# Enumerables {{{1
class Enumerable(object):
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


# SequenceEnumerable {{{1
class SequenceEnumerable(Enumerable):
    ''' sequence enumerable object '''

    def __init__(self, iterable):
        Enumerable.__init__(self, utils.tosequence(iterable))
        self._iter = iter(self._source)

    def __iter__(self):
        return SequenceEnumerable(self._source)

    def __next__(self):
        return compatible.next(self._iter)

    next = __next__

    def __len__(self):
        return self._source.__len__()

    def __getitem__(self, key):
        return self._source.__getitem__(key)

    def __contains__(self, item):
        return self._source.__contains__(item)


# OrderedEnumerable {{{1
class OrderedEnumerable(Enumerable):
    ''' ordered enumerable object '''

    def __init__(self, iterable, keys):
        Enumerable.__init__(self, iterable)
        self._keys = keys

    def __iter__(self):
        key = lambda x: list(map(lambda y: y(x), self._keys))
        return iter(sorted(self._source, key=key))



class List(list, Enumerable):
    ''' enumerable list object '''
    pass


class Dict(dict, Enumerable):
    ''' enumerable dict object '''
    pass


## Group {{{1
#class Group(Enumerable):
#    def __init__(self, enumerable, key):
#        Enumerable.__init__(self, enumerable)
#        self.key = key
#
#
## LookUp {{{1
#class LookUp(SequenceEnumerable):
#    def __init__(self, groups):
#        SequenceEnumerable.__init__(self, groups)
#

