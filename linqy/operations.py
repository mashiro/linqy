#()!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
from array import array
from linqy import compatible
from linqy import utils
from linqy.enumerable import Enumerable, SequenceEnumerable, OrderedEnumerable
from linqy.comparison import Comparison, Reverse
from linqy.decorators import extensionmethod, lazymethod
from linqy.function import Evaluator, Function
from linqy.undefined import _undefined

# Generation Operations {{{1
def make(iterable):
    if isinstance(iterable, Enumerable):
        # is enumerable
        return iterable
    elif utils.isgeneratorfunction(iterable):
        # is generator function
        return Enumerable(iterable)
    elif utils.issequence(iterable):
        # is sequence
        return SequenceEnumerable(iterable)
    else:
        # is iterable or generator
        return Enumerable(lambda: iter(iterable))

def empty():
    return make([])

@lazymethod(Enumerable)
def range(*args):
    s = slice(*args)
    return iter(compatible.irange(s.start or 0, s.stop or sys.maxsize, s.step or 1))

@lazymethod(Enumerable)
def repeat(item, count=None):
    if count is None:
        while True:
            yield item
    else:
        for i in compatible.irange(count):
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


# Sorting Operations {{{1
@extensionmethod(Enumerable)
def orderby(iterable, key=None, reverse=False):
    key = Function(key)
    if reverse:
        _key = lambda x: Reverse(key(x))
    else:
        _key = key
    return OrderedEnumerable(iterable, (_key,))

@extensionmethod(Enumerable)
def orderbydesc(iterable, key=None):
    return orderby(iterable, key=key, reverse=True)

@extensionmethod(OrderedEnumerable)
def thenby(iterable, key=None, reverse=False):
    key = Function(key)
    if reverse:
        _key = lambda x: Reverse(key(x))
    else:
        _key = key
    return OrderedEnumerable(iterable, iterable._keys + (_key,))

@extensionmethod(OrderedEnumerable)
def thenbydesc(iterable, key=None, reverse=False):
    return thenby(iterable, key=key, reverse=True)

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def reverse(iterable):
    return reversed(utils.tosequence(iterable))


# Set Operations {{{1
@extensionmethod(Enumerable)
def distinct(iterable, key=None):
    iterable = make(iterable)
    key = Function(key)
    keys = set()
    return (iterable
            .select(lambda x: [key(x), x])
            .where(lambda x: x[0] not in keys)
            .do(lambda x: keys.add(x[0]))
            .select(lambda x: x[1]))

@extensionmethod(Enumerable)
def union(first, second, key=None, all=False):
    iterable = concat(first, second)
    if all:
        return iterable
    else:
        return iterable.distinct(key)

@extensionmethod(Enumerable)
def unionall(first, second, key=None):
    return union(first, second, key, True)

@extensionmethod(Enumerable)
def except_(first, second, key=None):
    first = make(first)
    second = make(second)
    key = Function(key)
    keys = set(second.select(lambda x: key(x)))
    return (first
            .select(lambda x: [key(x), x])
            .where(lambda x: x[0] not in keys)
            .do(lambda x: keys.add(x[0]))
            .select(lambda x: x[1]))

@extensionmethod(Enumerable)
def intersect(first, second, key=None):
    first = make(first)
    second = make(second)
    key = Function(key)
    keys = set(second.select(lambda x: key(x)))
    return (first
            .select(lambda x: [key(x), x])
            .where(lambda x: x[0] in keys)
            .do(lambda x: keys.remove(x[0]))
            .select(lambda x: x[1]))


# Filtering Operatoins {{{1
@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def where(iterable, pred):
    pred = Function(pred)
    return compatible.ifilter(pred, iterable)

@extensionmethod(Enumerable)
def oftype(iterable, type):
    return where(iterable, lambda x: isinstance(x, type))


# Quantifier Operations {{{1
@extensionmethod(Enumerable)
def all(iterable, pred=None):
    pred = Function(pred)
    for x in compatible.ifilterfalse(pred, iterable):
        return False
    return True

@extensionmethod(Enumerable)
def any(iterable, pred=None):
    pred = Function(pred)
    for x in compatible.ifilter(pred, iterable):
        return True
    return False

@extensionmethod(Enumerable)
def contains(iterable, value, key=None):
    for x in select(iterable, key).where(lambda x: x == value):
        return True
    return False


# Projection Operations {{{1
@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def select(iterable, selector):
    selector = Function(selector)
    return compatible.imap(selector, iterable)

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def selectmany(iterable, selector, result=None):
    selector = Function(selector)
    result = Function(result)
    for x in iterable:
        for y in selector(x):
            if result:
                yield result(x, y)
            else:
                yield y

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def zip(iterable, *iterables):
    return compatible.izip(iterable, *iterables)

@extensionmethod(Enumerable)
def enumerate(iterable):
    return countup().zip(iterable)


# Partitioning Operations {{{1
@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def skip(iterable, count):
    return itertools.islice(iterable, count, None)

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def skipwhile(iterable, pred):
    pred = Function(pred or utils.always(True))
    return itertools.dropwhile(pred, iterable)

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def take(iterable, count):
    return itertools.islice(iterable, count)

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def takewhile(iterable, pred):
    pred = Function(pred or utils.always(True))
    return itertools.takewhile(pred, iterable)


# Join Operatoins {{{1
@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def join(outer, inner, outerkey, innerkey, result):
    raise NotImplementedError()

@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def groupjoin(outer, inner, outerkey, innerkey, result):
    raise NotImplementedError()


# Grouping Operations {{{1
@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def groupby(iterable, key, elem=None, result=None):
    result = Function(result)
    lookup = tolookup(iterable, key, elem)
    return select(lookup.items(), lambda k, v: result(k, v))


# Equality Operations {{{1
@extensionmethod(Enumerable)
def sequenceequal(first, second, selector=None):
    selector = Function(selector)
    first, second = compatible.imap(list, [first, second])
    if len(first) != len(second):
        return False
    for a, b in compatible.izip(first, second):
        if selector(a) != selector(b):
            return False
    return True


# Element Operations {{{1
@extensionmethod(Enumerable)
def elementat(iterable, index, default=_undefined):
    try:
        return compatible.next(iter(skip(iterable, index)), default)
    except StopIteration:
        raise IndexError('enuemrable index out of range')

@extensionmethod(Enumerable)
def first(iterable, pred=None, default=_undefined):
    pred = Function(pred or utils.always(True))
    return where(iterable, pred).elementat(0, default)

@extensionmethod(Enumerable)
def last(iterable, pred=None, default=_undefined):
    pred = Function(pred or utils.always(True))
    return reverse(iterable).first(pred, default)

@extensionmethod(Enumerable)
def single(iterable, pred=None, default=_undefined):
    iterator = iter(where(iterable, pred))
    try:
        result = compatible.next(iterator)
    except StopIteration:
        if default is not _undefined:
            return default
        raise LookupError('enumerable contains no matching element')
    else:
        try:
            compatible.next(iterator)
            raise LookupError('enumerable contains more than one element')
        except StopIteration:
            return result


# Converting Operations {{{1
@extensionmethod(Enumerable)
def toarray(iterable, typecode):
    return array(typecode, iterable)

@extensionmethod(Enumerable)
def tolist(iterable):
    return list(iterable)

@extensionmethod(Enumerable)
def todict(iterable, key=None, elem=None):
    key = Function(key)
    elem = Function(elem)
    return dict([(key(item), elem(item)) for item in iterable])

@extensionmethod(Enumerable)
def tolookup(iterable, key=None, elem=None):
    key = Function(key)
    elem = Function(elem)
    lookup = dict()
    for item in iterable:
        k = key(item)
        v = elem(item)
        group = lookup.setdefault(k, list())
        group.append(v)
    return lookup


# Concatenation Operations {{{1
@extensionmethod(Enumerable)
@lazymethod(Enumerable)
def concat(iterable, *iterables):
    return itertools.chain(iterable, *iterables)


# Aggregation Operations {{{1
@extensionmethod(Enumerable)
def aggregate(iterable, func, selector=None, seed=_undefined):
    func = Function(func)
    selector = Function(selector)
    if seed is _undefined:
        return selector(compatible.reduce(func, iterable))
    else:
        return selector(compatible.reduce(func, iterable, seed))

@extensionmethod(Enumerable)
def average(iterable, selector=None):
    seq = make(list(iterable))
    return seq.sum(selector) / seq.count()

@extensionmethod(Enumerable)
def count(iterable, pred=None):
    pred = Function(pred or utils.always(True))
    return compatible.reduce(lambda n, _: n + 1, where(iterable, pred), 0)

@extensionmethod(Enumerable)
def max(iterable, selector=None):
    return compatible.max(select(iterable, selector))

@extensionmethod(Enumerable)
def min(iterable, selector=None):
    return compatible.min(select(iterable, selector))

@extensionmethod(Enumerable)
def sum(iterable, selector=None):
    return compatible.sum(select(iterable, selector))


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


# Helpers {{{1
def extend(type, *funcs):
    if len(funcs) == 0:
        funcs = Enumerable._operations.values()
    for func in funcs:
        extensionmethod(type)(func)


# End {{{1
__all__ = list(Enumerable._operations.keys()) + [
    'make',
    'empty',
    'range',
    'repeat',
    'cycle',
    'countup',
    'extend',
]

