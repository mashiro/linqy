#!/usr/bin/env python
# -*- coding: utf-8 -*-
import linqy

def main():
    value = 10
    query = 'value * _ * 2'

    f = linqy.Q(query)
    print f(11)

if __name__ == '__main__':
    main()

