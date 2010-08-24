#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import urllib
import simplejson
import linqy
from linqy.functors import *

def enumerate_line(response):
	while True:
		yield response.readline()

def sample_stream():
	response = urllib.urlopen('http://stream.twitter.com/1/statuses/sample.json')
	query = linqy.make(enumerate_line(response),
		where(lambda s: s is not None and len(s) > 0),
		select(lambda s: s.decode('utf-8')),
		select(lambda s: simplejson.loads(s)))
	return iter(query)

def main():
	stream = linqy.make(sample_stream())
	ids = stream.take(1)
	statuses = stream.combine(
		where(lambda s: 'user' in s),
		select(lambda s: {'name': s['user']['screen_name'], 'text': s['text']}))
	for status in statuses:
		print '%s: %s' % (status['name'], status['text'])

if __name__ == '__main__':
	main()

