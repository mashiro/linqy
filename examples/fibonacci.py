#!/usr/bin/env python
# -*- coding: utf-8 -*-
import linqy

def fibonacci():
    yield 0
    yield 1
    fibs = linqy.make(fibonacci)
    query = (fibs.zip(fibs.skip(1))
            .select(lambda item: item[0] + item[1]))
    for item in query:
        yield item

def main():
    for n, i in linqy.make(fibonacci).enumerate():
        print '%d: %d' % (i, n)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

