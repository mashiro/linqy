#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
from array import array
from linqy.function import *
from linqy.comparison import *
from linqy.utils import *

# Enumerables {{{1
class Enumerable(object):
    ''' enumerable object '''

    def __init__(self, generator):
        self._generator = generator

    def __iter__(self):
        return self._generator()

class SequenceEnumerable(Enumerable):
    ''' sequence enumerable object '''

    def __init__(self, sequence):
        self._sequence = sequence
        self._index = 0

    def __iter__(self):
        return SequenceEnumerable(self._sequence)

    def __next__(self):
        if self._index < len(self._sequence):
            result = self._sequence[self._index]
            self._index += 1
            return result
        raise StopIteration

    next = __next__

    def __len__(self):
        return self._sequence.__len__()

    def __getitem__(self, key):
        return self._sequence.__getitem__(key)

    def __contains__(self, item):
        return self._sequence.__contains__(item)

class OrderedEnumerable(Enumerable):
    ''' ordered enumerable object '''

    def __init__(self, iterable, key, reverse, parent=None):
        self._iterable = iterable
        self._key = key
        self._reverse = reverse
        self._parent = parent

    def __iter__(self):
        def key(context):
            if context._reverse:
                return lambda x: Reverse(context._key(x))
            else:
                return lambda x: context._key(x)

        keys = [key(context) for context in self.contexts()]
        func = lambda x: tuple(imap(lambda key: key(x), keys))
        return iter(sorted(self._iterable, key=func))

    def contexts(self):
        results = []
        context = self
        while context is not None:
            results.append(context)
            context = context._parent
        return reversed(results)


# Decolators {{{1
def extensionmethod(type):
    def outer(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        setattr(type, func.__name__, inner)
        return func
    return outer

def lazymethod(type):
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            return type(lambda: func(*args, **kwargs))
        return inner
    return outer


# Generation Operations {{{1
def make(iterable):
    return asenumerable(iterable)

def empty():
    return make([])

@lazymethod(Enumerable)
def range(*args):
    s = slice(*args)
    return iter(irange(s.start or 0, s.stop or sys.maxsize, s.step or 1))

@lazymethod(Enumerable)
def repeat(item, count=None):
    if count is None:
        while True:
            yield item
    else:
        for i in irange(count):
            yield item

@lazymethod(Enumerable)
def cycle(iterable):
    return itertools.cycle(iterable)

@lazymethod(Enumerable)
def countup(start=0, step=1):
    n = start
    while True:
        yield n
        n += step


# Projection Operations {{{1
@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def select(iterable, selector):
    return imap(Function(selector), iterable)

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def selectmany(iterable, selector, result=None):
    selector = Function(selector)
    result = Function(result)
    for x in asenumerable(iterable):
        for y in selector(x):
            if result:
                yield result(x, y)
            else:
                yield y

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def zip(iterable, *iterables):
    return izip(iterable, *iterables)

@extensionmethod(Enumerable)
def enumerate(iterable):
    return countup().zip(iterable)


# Filtering Operatoins {{{1
@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def where(iterable, pred=None):
    return ifilter(Function(pred), iterable)

@extensionmethod(Enumerable)
def oftype(iterable, type):
    return where(iterable, lambda x: isinstance(x, type))


# Partitioning Operations {{{1
@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def skip(iterable, count):
    return itertools.islice(iterable, count, None)

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def skipwhile(iterable, pred=None):
    return itertools.dropwhile(Function(pred), iterable)

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def take(iterable, count):
    return itertools.islice(iterable, count)

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def takewhile(iterable, pred=None):
    return itertools.takewhile(Function(pred), iterable)


# Ordering Operations {{{1
@extensionmethod(Enumerable)
def orderby(iterable, key=None, reverse=False):
    return OrderedEnumerable(iterable, key, reverse)

@extensionmethod(Enumerable)
def orderby_descending(iterable, key=None):
    return orderby(iterable, key=key, reverse=True)

@extensionmethod(OrderedEnumerable)
def thenby(ordered, key=None, reverse=False):
    return OrderedEnumerable(ordered._iterable, key, reverse, ordered)

@extensionmethod(OrderedEnumerable)
def thenby_descending(ordered, key=None, reverse=False):
    return thenby(ordered, key=key, reverse=True)

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def reverse(iterable):
    return reversed(tosequence(iterable))


# Concatenation Operations {{{1
@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def concat(iterable, *iterables):
    return itertools.chain(iterable, *iterables)


# Equality Operations {{{1
@extensionmethod(Enumerable)
def sequenceequal(first, second, selector=None):
    selector = Function(selector)
    first, second = imap(list, [first, second])
    if len(first) != len(second):
        return False
    for a, b in izip(first, second):
        if selector(a) != selector(b):
            return False
    return True


# Quantifier Operations {{{1
@extensionmethod(Enumerable)
def all(iterable, pred=None):
    for x in ifilterfalse(Function(pred), iterable):
        return False
    return True

@extensionmethod(Enumerable)
def any(iterable, pred=None):
    for x in ifilter(Function(pred or always(True)), iterable):
        return True
    return False

@extensionmethod(Enumerable)
def contain(iterable, value):
    return value in tosequence(iterable)


# Element Operations {{{1
@extensionmethod(Enumerable)
def elementat(iterable, index, default=Undefined):
    try:
        return next(iter(skip(iterable, index)), default)
    except StopIteration:
        raise IndexError('enuemrable index out of range')

@extensionmethod(Enumerable)
def first(iterable, pred=None, default=Undefined):
    return where(iterable, Function(pred)).elementat(0, default)

@extensionmethod(Enumerable)
def last(iterable, pred=None, default=Undefined):
    return reverse(iterable).first(pred, default)

@extensionmethod(Enumerable)
def single(iterable, pred=None, default=Undefined):
    items = where(iterable, Function(pred)).tolist()
    if len(items) == 0:
        if default is Undefined:
            raise ValueError('enumerable contains no matching element')
        else:
            return default
    elif len(items) == 1:
        return items[0]
    else:
        raise ValueError('enumerable contains more than one element')


# Converting Operations {{{1
@extensionmethod(Enumerable)
def asenumerable(iterable):
    if isinstance(iterable, Enumerable):
        # is enumerable
        return iterable
    elif isgenerator(iterable) or isgeneratorfunction(iterable):
        # is generator or generator function
        return Enumerable(iterable)
    elif issequence(iterable):
        # is sequence
        return SequenceEnumerable(iterable)
    else:
        # is iterable
        return Enumerable(lambda: iter(iterable))

@extensionmethod(Enumerable)
def toarray(iterable, typecode):
    return array(typecode, iterable)

@extensionmethod(Enumerable)
def tolist(iterable):
    return list(iterable)


# Action Operations {{{1
@extensionmethod(Enumerable)
def foreach(iterable, action):
    action = Function(action)
    for item in iterable:
        action(item)

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def do(iterable, action):
    action = Function(action)
    for item in iterable:
        action(item)
        yield item

