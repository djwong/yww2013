#!/usr/bin/python

# Take a html template, a dance program, and dance cribs, and generate the html
# part of an interactive cribsheet.  (CSS+JS still required.)
# Copyright 2013 Darrick J. Wong.  All rights reserved.

# Dance program file format:
# I: <description of interlude>
# D: <name of dance>

# Dance crib file format:
# Name: <name of dance>
# Format: <what kind of dance -- 8x32R, 4x32S, etc>
# Source: <where you got it from>
# <bars>	<steps>
#
# Note: Any line not starting with Name:/Format:/Source: is assumed to be
# the start of dance figure instructions.
#
# Dance crib files should be cribs/<filename_of_dance>.txt
# wherein the "name of dance" above has been converted to lowercase, the
# spaces replaced with underscores, and all non alphanumeric letters removed.
# Hence, "Postie's Jig" becomes "cribs/posties_jig.txt".

import sys

if len(sys.argv) == 1 or len(sys.argv) > 1 and sys.argv[1] == "--help":
	print "Usage: %s template" % sys.argv[0]
	sys.exit(0)

def write_dance(dance_name, dance_number, output):
	dance_fname = 'cribs/'
	for letter in dance_name.lower():
		if letter.isalnum():
			dance_fname = dance_fname + letter
		elif letter == ' ':
			dance_fname = dance_fname + '_'
	dance_fname = dance_fname + '.txt'
	in_instructions = False
	source = ''
	with file(dance_fname) as dancefile:
		for danceline in dancefile:
			danceline = danceline.strip()
			if in_instructions:
				x = danceline.partition('	')
				output.write('	<tr><td class="crib_step_bars">%s</td><td>%s</td>\n' % (x[0], x[2]))
			elif danceline.startswith("Name: "):
				name = danceline[6:]
			elif danceline.startswith("Format: "):
				fmt = danceline[8:]
			elif danceline.startswith("Source: "):
				source = danceline[8:]
			else:
				in_instructions = True
				output.write('<tr class="crib_header" onclick="crib_toggle(\'crib%d\');"><td><span id="crib%d_ctl" class="crib_ctl">&#9654;</span><span class="crib_name">%s</span> (%s)</td><td>%s</td></tr>\n' % (dance_number, dance_number, name, fmt, source))
				output.write('<tr id="crib%d" class="crib_steps"><td colspan="2">\n' % dance_number)
				output.write('	<table class="crib_step_table">\n')
				x = danceline.partition('	')
				output.write('	<tr><td class="crib_step_bars">%s</td><td>%s</td>\n' % (x[0], x[2]))
		if in_instructions:
			output.write('	</table>\n')
			output.write('</td></tr>\n')

with file(sys.argv[2], "w") as output:
	dance_number = 0
	for line in file(sys.argv[1]):
		if not line[:5] == "CRIB:":
			output.write(line)
			continue
		crib_fname = line[5:].strip()
		with file(crib_fname) as cribfile:
			output.write('<table class="crib_table">\n')
			for cribline in cribfile:
				if cribline[:3] == "I: ":
					output.write('<tr class="crib_interlude"><td colspan="2">' + cribline[3:].strip() + '</td></tr>\n')
				elif cribline[:3] == "D: ":
					write_dance(cribline[3:].strip(), dance_number, output)
					dance_number = dance_number + 1
			output.write('</table>\n');