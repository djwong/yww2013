#!/usr/bin/env python3

# Take a crib description file and generate an interactive HTML crib sheet.
# CSS/JS are still required.  This is NOT QUITE the same script as was on the
# Youth Weekend West 2013 site.
# Copyright 2013 Darrick J. Wong.  All rights reserved.

# Dance program file format:
# I: <description of interlude>
# D: <name of dance>

# Dance crib file format:
# Name: <name of dance>
# Format: <what kind of dance -- 8x32R, 4x32S, etc>
# Source: <where you got it from>
# Youtube: <the youtube video id>
# Endnote: Notes to put at the end 
# <other key: value pairs which are copied verbatim>
# BARS
# <bars>\tab	<steps>
#
# Dance crib files should be dances/<filename_of_dance>.txt
# wherein the "name of dance" above has been converted to lowercase, the
# spaces replaced with underscores, and all non alphanumeric letters removed.
# Hence, "Postie's Jig" becomes "dances/posties_jig.txt".
#
# Look for anything with "crib_" in the name in style2.css and site2.js,
# if you're trying to extract the crib generator code.

import sys
import cgi
import hashlib
import uuid
import os
import re

DEBUG=' border=1'
DEBUG=''

def write_dance(dance_name, output):
	dance_fname = 'dances/'
	for letter in dance_name.lower():
		if letter.isalnum():
			dance_fname = dance_fname + letter
		elif letter == ' ':
			dance_fname = dance_fname + '_'
	dance_fname = dance_fname + '.txt'
	alg = hashlib.sha1()
	alg.update(str(uuid.uuid4()).encode('utf-8'))
	dance_id = alg.hexdigest()
	with open(dance_fname) as dancefile:
		in_instructions = False
		props = {}
		for danceline in dancefile:
			line = danceline.strip()
			if len(line) == 0 or line[0] == '#':
				continue
			elif in_instructions:
				(bars, sep, figure) = line.partition('\t')
				bars = re.sub(r'\s*-\s*', '-', bars.strip())
				output.write('	<tr><td class="crib_step_bars">%s</td>\n' % cgi.escape(bars))
				output.write('	<td class="crib_step_figures">%s</td></tr>\n' % cgi.escape(figure))
			elif line == 'BARS':
				in_instructions = True

				# Dance file missing any keys?
				reqd_keys = set(['Name', 'Format', 'Source'])
				found_keys = set(props) & reqd_keys
				missing_keys = found_keys ^ reqd_keys
				if missing_keys:
					raise Exception("%s: Missing required keys: %s" % (dance_fname, missing_keys))

				# Set up youtube links
				youtube_str = ''
				if 'Youtube' in props:
					youtube_str = '<span class="crib_youtube">&nbsp;[<a href="http://www.youtube.com/watch?v=%s">video</a>]</span>' % props['Youtube']

				# Emit dance header
				output.write('<tr class="crib_header">\n')
				output.write('<td><span id="crib_%s_ctl" class="crib_ctl" onclick="crib_toggle(\'crib_%s\');">&#9654;</span></td>\n' % (dance_id, dance_id))
				output.write('<td class="crib_name_cell"><div><span class="crib_name" onclick="crib_toggle(\'crib_%s\');">%s</span>%s</div><div class="crib_source">%s</div></td>\n' % (dance_id, cgi.escape(props['Name']), youtube_str, cgi.escape(props['Source'])))
				output.write('<td class="crib_format">%s</td>\n' % cgi.escape(props['Format']))
				output.write('</tr>\n')

				output.write('<tr id="crib_%s" class="crib_steps"><td></td><td style="padding: 0px;" colspan="2">\n' % dance_id)
				output.write('	<table class="crib_step_table"%s>\n' % DEBUG)
				for key in props:
					if key in ['Youtube', 'Name', 'Format', 'Source', 'Endnote']:
						continue
					output.write('	<tr><td class="crib_note" colspan="2"><b>%s:</b> %s</td></tr>\n' % (cgi.escape(key), cgi.escape(props[key])))
			else:
				(key, sep, value) = line.partition(': ')
				props[key] = value

		if in_instructions:
			output.write('	</table>\n')
			if 'Endnote' in props:
				output.write('<p>%s</p>\n' % cgi.escape(props['Endnote']))
			output.write('</td></tr>\n')

def generate_crib(cribfd, outfd):
	'''Given an input crib file, generate an output.'''

	outfd.write('<table class="crib_table"%s>\n' % DEBUG)
	for cribline in cribfd:
		if cribline[0] == '#':
			continue
		elif cribline[:3] == "I: ":
			outfd.write('<tr class="crib_interlude"><td colspan="3">' + cgi.escape(cribline[3:].strip()) + '</td></tr>\n')
		elif cribline[:3] == "D: ":
			write_dance(cribline[3:].strip(), outfd)
	outfd.write('</table>\n');

def inject_cribs(templatefd, outfd):
	'''Given a template file full of CRIB: statements, paste in the cribs.'''

	for line in templatefd:
		if not line[:5] == "CRIB:":
			outfd.write(line)
			continue
		crib_fname = line[5:].strip()
		generate_crib(open(crib_fname), outfd)

def print_help():
	print("Usage: %s [-i template outfile|-g templates...]" % sys.argv[0])
	sys.exit(0)

# Main code
if __name__ == '__main__':
	if len(sys.argv) == 1 or '--help' in sys.argv:
		print_help()

	if sys.argv[1] == '-i' and len(sys.argv) == 4:
		inject_cribs(open(sys.argv[2]), open(sys.argv[3], 'w'))
	elif sys.argv[1] == '-g' and len(sys.argv) > 2:
		for fname in sys.argv[2:]:
			dot_location = fname.rfind('.')
			if dot_location >= 0:
				outfname = fname[:dot_location] + ".crib"
			else:
				outfname = fname + ".crib"
			try:
				generate_crib(open(fname), open(outfname, 'w'))
			except Exception as e:
				print(e)
				os.remove(outfname)
				sys.exit(1)
	else:
		print_help()
