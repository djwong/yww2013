#!/usr/bin/python

# Take a html template, a dance program, and dance cribs, and generate the
# Makefile dependencies for it.  See crib.py for file format documentation.
# Copyright 2013 Darrick J. Wong.  All rights reserved.

import sys

def write_dance(dance_name, output):
	dance_fname = 'dances/'
	for letter in dance_name.lower():
		if letter.isalnum():
			dance_fname = dance_fname + letter
		elif letter == ' ':
			dance_fname = dance_fname + '_'
	output.write('%s.txt ' % dance_fname)

if __name__ == "__main__":
	if len(sys.argv) != 4 or (len(sys.argv) > 1 and sys.argv[1] == "--help"):
		print "Usage: %s template target output" % sys.argv[0]
		sys.exit(0)

	dance_number = 0
	with file(sys.argv[3], 'w') as output:
		output.write('%s: ' % sys.argv[2])
		for cribline in file(sys.argv[1]):
			if cribline[:3] == "D: ":
				write_dance(cribline[3:].strip(), output)
		output.write('\n')
