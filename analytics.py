#!/usr/bin/python

import re
import csv
import sys
import urllib
import datetime

if len(sys.argv) < 2 or sys.argv[1] == '--help':
	print "Usage: %s csvfile [--html]" % sys.argv[0]
	sys.exit(1)

mode = 'text'
if len(sys.argv) > 2:
	if sys.argv[2] == '--html':
		mode = 'html'
	else:
		print "Usage: %s csvfile [--html]" % sys.argv[0]
		sys.exit(1)

# CSV Columns: timestamp name age gender allergies address phone email contact
# parental package payment paypal years_dancing freq_dancing elective
# walkthrough ceildh ceildh_act roommates other superstar crap; do

questions = None
records = []
q_order = ['timestamp', 'age', 'gender', 'address', 'contact', 'package', \
	 'payment', 'years_dancing', 'freq_dancing', 'elective', \
	 'walkthrough', 'ceildh', 'superstar']
regions = {
	re.compile('[ ,]OR[ \n]*'): 'Oregon',
	re.compile('[ ,]BC[ \n]*'): 'British Columbia',
	re.compile('[ ,]WA[ \n]*'): 'Washington',
	re.compile('[ ,]CA[ \n]*'): 'California',
}

# Transform file data into a bunch of key-value groups
first_row = True
with open(sys.argv[1], 'rb') as csvfile:
	csvreader = csv.reader(csvfile)
	for row in csvreader:
		if first_row:
			first_row = False
			questions = {
				'timestamp': 'When did you register?',
				'age': row[2],
				'gender': 'Gender?',
				'address': 'Where are you from?',
				'contact': row[8],
				'package': row[10],
				'payment': row[11],
				'years_dancing': row[13],
				'freq_dancing': row[14],
				'elective': row[15],
				'walkthrough': row[16],
				'ceildh': row[17],
				'superstar': row[21],
			}
			continue
		if row[1][:6] == 'Ignore' or \
		   row[10] == 'Dinner + Ball':
			continue
	
		# Filter some of the data
		superstar = row[21]
		if superstar == '':
			superstar = 'No, thank you.'
		address = row[5]
		addr = address.upper()
		for rx in regions:
			if rx.search(addr) != None:
				address = regions[rx]
				break
		if addr == '':
			address = 'Unknown'
		package = row[10]
		if package == 'Class + Dinner + All Dancing Events + Lodging':
			package = 'Hotel + All Events'
		elif package == 'Class + Dinner + All Dancing Events':
			package = 'All Events'
		try:
			age = int(row[2])
			if age <= 18:
				age = '0-18'
			elif age > 18 and age <= 25:
				age = '19-25'
			elif age > 25 and age <= 30:
				age = '26-30'
			else:
				age = '31+'
		except:
			age = row[2]
		timestamp = row[0][:1]
		if timestamp == '2':
			timestamp = 'February'
		elif timestamp == '3':
			timestamp = 'March'
		elif timestamp == '4':
			timestamp = 'April'
		elif timestamp == '5':
			timestamp = 'May'
		record = {
			'timestamp': timestamp,
			'age': age,
			'gender': row[3],
			'address': address,
			'contact': row[8],
			'package': package,
			'payment': row[11],
			'years_dancing': row[13],
			'freq_dancing': row[14],
			'elective': row[15],
			'walkthrough': row[16],
			'ceildh': row[17],
			'superstar': superstar,
		}
		records.append(record)

# Summarize records
responses = {}
for record in records:
	for key in record:
		if key not in responses:
			responses[key] = {}
		value = record[key]
		if value not in responses[key]:
			responses[key][value] = 0
		responses[key][value] = responses[key][value] + 1

# Do a little sanity checking:
num_replies = len(records)
for q_key in q_order:
	x = 0
	for response in responses[q_key]:
		x = x + responses[q_key][response]
	assert x == num_replies

# Print report
def report_text():
	for q_key in q_order:
		print questions[q_key]
		r_keys = responses[q_key].keys()
		r_keys.sort()
		for response in r_keys:
			print '%s: %.0f%%' % (response,
				100.0 * responses[q_key][response] / num_replies)
		print ''

def report_html():
	print '<h1>Analytics</h1>'
	print '<p>A little bit of aggregated information about the %d people registered, as of %s.</p>' % (num_replies, datetime.datetime.now().strftime('%c'))
	for q_key in q_order:
		print '<h2>%s</h2>' % questions[q_key]
		r_keys = responses[q_key].keys()
		r_keys.sort()
		chd = None
		chl = None
		for response in r_keys:
			# Numbers
			if chd == None:
				chd = 't:%d' % responses[q_key][response]
			else:
				chd = chd + ',%d' % responses[q_key][response]
			# Labels
			if chl == None:
				chl = '%s (%.0f%%)' % (response, 100.0 * responses[q_key][response] / num_replies)
			else:
				chl = chl + '|%s (%.0f%%)' % (response, 100.0 * responses[q_key][response] / num_replies)
		chd = urllib.quote_plus(chd, '|,:')
		chl = urllib.quote_plus(chl, '|,:')
		url = 'http://chart.googleapis.com/chart?cht=p&amp;chs=640x200&amp;chco=5f7ca8&amp;chdls=000000,18&amp;chds=a&amp;chd=%s&amp;chl=%s' % (chd, chl)
		print '<img src="%s" alt="%s"></img>' % (url, questions[q_key])
		print ''

x = "report_%s()" % mode
eval(x)
sys.exit(0)