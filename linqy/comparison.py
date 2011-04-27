#!/usr/bin/env python
# -*- coding: utf-8 -*-
from linqy.utils import not_

class Comparison(object):
    def __init__(self, key):
        self.key = key

    def __eq__(self, other):
        return self.key == other.key

    def __ne__(self, other):
        return self.key != other.key

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key

    def __gt__(self, other):
        return self.key > other.key

    def __ge__(self, other):
        return self.key >= other.key


class Reverse(Comparison):
    __lt__ = not_(Comparison.__lt__)
    __le__ = not_(Comparison.__le__)
    __gt__ = not_(Comparison.__gt__)
    __ge__ = not_(Comparison.__ge__)

