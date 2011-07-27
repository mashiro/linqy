#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Linqy - LINQ like library for Python '''

from linqy.meta import __author__, __email__, __license__, __version__, __url__

from linqy.enumerable import Enumerable, SequenceEnumerable, OrderedEnumerable
from linqy.function import Evaluator, Function, Q
from linqy.decorators import extensionmethod, lazymethod
from linqy.utils import anonymous
from linqy.operations import *

