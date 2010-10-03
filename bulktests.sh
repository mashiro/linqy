#!/bin/sh

bins="python2.4 python2.5 python2.6 python2.7 python3.1"
testcase="tests.py"

for bin in $bins; do
	echo $bin
	`$bin $testcase`
	echo
done

