#!/usr/bin/env python3

# Take a html template, a dance program, and dance cribs, and generate the
# Makefile dependencies for it.  See crib.py for file format documentation.
# Copyright 2013 Darrick J. Wong.  All rights reserved.

import sys

if len(sys.argv) != 4 or len(sys.argv) > 1 and sys.argv[1] == "--help":
	print("Usage: %s template outputfile make_target" % sys.argv[0])
	sys.exit(0)

def write_dance(dance_name, dance_number, output):
	dance_fname = 'dances/'
	for letter in dance_name.lower():
		if letter.isalnum():
			dance_fname = dance_fname + letter
		elif letter == ' ':
			dance_fname = dance_fname + '_'
	output.write('%s.txt ' % dance_fname)

with open(sys.argv[2], "w") as output:
	output.write('%s: ' % sys.argv[3])
	dance_number = 0
	for line in open(sys.argv[1]):
		if not line[:5] == "CRIB:":
			continue
		crib_fname = line[5:].strip()
		output.write('%s ' % crib_fname)
		with open(crib_fname) as cribfile:
			for cribline in cribfile:
				if cribline[:3] == "D: ":
					write_dance(cribline[3:].strip(), dance_number, output)
					dance_number = dance_number + 1
	output.write('\n')
