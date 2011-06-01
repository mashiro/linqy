#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Linqy - LINQ like library for Python '''

__author__ = 'mashiro'
__email__ = 'y.mashiro@gmail.com'
__license__ = 'MIT'
__version__ = '0.3.0'
__url__ = 'http://github.com/mashiro/linqy'

from linqy.enumerable import Enumerable, SequenceEnumerable, OrderedEnumerable
from linqy.function import Evaluator, Function, Q
from linqy.decorators import extensionmethod, lazymethod
from linqy.utils import anonymous
from linqy.operations import *

