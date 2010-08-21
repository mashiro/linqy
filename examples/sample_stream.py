#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import urllib
import simplejson
import linqy

def enumerate_line(response):
	buf = ''
	while True:
		c = response.read(1)
		if c == '\n':
			yield buf
			buf = ''
		else:
			buf += c

def sample_stream():
	response = urllib.urlopen('http://stream.twitter.com/1/statuses/sample.json')
	query = linqy.make(enumerate_line(response),
		linqy.where(lambda s: s is not None and len(s) > 0),
		linqy.select(lambda s: s.decode('utf-8')),
		linqy.select(lambda s: simplejson.loads(s)))
	for item in query:
		yield item

def main():
	stream = linqy.make(sample_stream())
	ids = stream.take(1)
	statuses = stream.combine(
		linqy.where(lambda s: 'user' in s),
		linqy.select(lambda s: {'name': s['user']['screen_name'], 'text': s['text']}))
	for status in statuses:
		print '%s: %s' % (status['name'], status['text'])

if __name__ == '__main__':
	main()

