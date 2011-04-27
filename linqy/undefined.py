#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Undefined(object):
    pass

def isundefined(object):
    return isinstance(object, Undefined)

