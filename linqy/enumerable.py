#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Enumerables {{{1
class Enumerable(object):
    ''' enumerable object '''

    def __init__(self, generator):
        self._source = generator

    def __iter__(self):
        return self._source()

    @classmethod
    def __extend__(cls, name, func):
        if not hasattr(cls, '_operators'):
            cls._operators = {}
        cls._operators[name] = func
        setattr(cls, name, func)


# SequenceEnumerable {{{1
class SequenceEnumerable(Enumerable):
    ''' sequence enumerable object '''

    def __init__(self, sequence):
        Enumerable.__init__(self, sequence)
        self._index = 0

    def __iter__(self):
        return SequenceEnumerable(self._source)

    def __next__(self):
        if self._index < len(self._source):
            result = self._source[self._index]
            self._index += 1
            return result
        raise StopIteration

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


