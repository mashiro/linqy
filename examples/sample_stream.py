#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import linqy
try:
    import json
except ImportError:
    import simplejson as json

def enumerate_line(response):
    while True:
        yield response.readline()

def sample_stream():
    response = urllib.urlopen('http://stream.twitter.com/1/statuses/sample.json')
    return (linqy.make(enumerate_line(response))
            .where(lambda s: s)
            .select(lambda s: s.decode('utf-8'))
            .select(lambda s: json.loads(s)))

def main():
    stream = sample_stream()
    statuses = (stream
            .where(lambda s: 'user' in s)
            .select(lambda s: linqy.anonymous(
                name=s['user']['screen_name'],
                text=s['text'])))

    # subscribe
    for status in statuses:
        print '%s: %s' % (status.name, status.text)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

