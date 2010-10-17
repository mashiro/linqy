#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Linqy - LINQ like library for Python '''

__author__ = 'mashiro'
__email__ = 'y.mashiro@gmail.com'
__license__ = 'MIT'
__version__ = '0.2.6'
__url__ = 'http://github.com/mashiro/linqy'

from linqy.enumerable import (
        Enumerable, SequenceEnumerable, OrderedEnumerable,
        extensionmethod, lazymethod,
        make, empty, range, repeat, cycle, countup,
        select, selectmany, zip, enumerate,
        where, oftype,
        skip, skipwhile, take, takewhile,
        orderby, orderby_descending, thenby, thenby_descending, reverse,
        sequenceequal,
        all, any, contain,
        elementat, first, last, single,
        asenumerable, toarray, tolist,
        foreach, do)
from linqy.function import Evaluator, Function, Not
from linqy.utils import anonymous

