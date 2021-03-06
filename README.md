yww2013
=======

This is the Youth Weekend 2013 website repository.  There's a Makefile that
describes (to the computer) how to transform web page templates (.html.in
files) into finished HTML pages (.html files), build the web cribs from textual
descriptions, and prepare consistent styling across the website.

The Makefile assumes that you're running it on a fairly standard Linux system
with GNU make, bash (both needed for build automation), python 2 (scripting),
and lftp (uploading to FTP site).

After cloning this repository, run "make install" to build all the HTML files
and copy the miscellaneous blobs to the "output" directory.  Then simply rsync
the output directory to the desired web host via "make upload".

HTML Templating
===============
Each page's contents live in .html.in files.  These files should contain the
body portions of the HTML, as the header and footer will be attached during the
assembly process.

The headers are generated by the generate_header script, which puts a specific
title, picture, and caption at the top of every page.  This is the first
content to be written to the .html file.  The file "files" is a
semicolon-separated flat file that supplies attributes of each page on the
site:

The columns are as follows:
 1. filename
 2. title
 3. obsolete (if yes, put a yellow banner disclaiming old contents at the top)
 4. visible (if yes, put a navigation link at the top)
 5. background (path to the picture at the top of the page, minus ".jpg")
 6. background-descr (description of the background picture)
 7. private (if yes, put a red banner at the top warning it's a private page)

Next, the .html.in content is written to the .html file.  Finally, the footer,
which lives in the file "footer", is written to the .html file.

Analytics
=========
There's also an analytics script that parses the registration database to spit
out some handy graphs about who's coming.  You probably want to make your own
copy of that spreadsheet and update the URL underneath "registration.csv:" in
the Makefile.  Have a look at analytics.py if you want details.

Cribs
=====
The HTML cribs are generated with Python scripts from text files.  A (somewhat
newer) version runs portlandscottishdancers.org now; check with Darrick for a
refresh of individual dance descriptions.

The site is set up to generate two cribs: one for the ceilidh and one for the
ball.  There are two files, ceilidh.txt and ball.txt, which list the dances:

	D: Reel of the 51st Division
	D: The Flowers of Edinburgh
	I: Ending Waltz

A line starting with "I: " will have the rest of the line copied straight into
the HTML crib.  A line starting with "D: " is used to find a dance description.
To find a dance description, take the name of the dance, convert spaces (' ')
to underscores ('_'), the uppercase letters to lowercase, and remove the
punctuation.  This file will be found in the dances/ directory with ".txt"
after it.  Therefore, the instructions for "D: Miss Milligan's S'spey" are in
"dances/miss_milligans_sspey.txt".

The dance files themselves consist of a few lines of colon-delimited key-value
pairs establishing metadata about the dance, the word "BARS" on a line by
itself, and then a bar count, a tab, and the instructions for those bars.
Each dance MUST have at least a "Name", a "Format", and a "Source".  Other
possible keys are "Youtube" (videos), and "Notes" (general notes).  A sample
would look like this:

	Name: Miss Milligan’s Strathspey
	Youtube: qlNjsQAKff8
	Format: 8×32S, 3C (4C set)
	Source: Golden Jubilee Dances
	BARS
	1-8	1s+2s circle 4H round to left, 1s turn to face 2s & set, 1s cast while 2s dance up
	9-16	2s+1s+3s dance reflection reels of 3 on own sides 1s dancing in between 3s to start
	17-24	2s+1s+3s set, 2s+1s ½ turn LH, 1s followed by 2s lead down between 3s, cross & cast up on own sides
	25-32	1s+2s dance the Knot

(Note that this format enables fairly easy cut-and-paste from the Scottish
Dance Dictionary site.)

crib.py does all the magic of turning these text files into HTML snippets,
which are then embedded into the HTML.

Registration Form
=================
We let Google Sheets/Forms handle the registration database.  You can (could?)
use Sheets to create a HTML form, which we massaged into the file
register.html.in.old, then I added bits to call out to Paypal for payment
handling.  It's a bit clunky but it was integrated acceptably.  I left comments
marking the parts I altered.

We highly recommend making the Register link on all the pages bright red when
registration is open and gray when it's not.  See the "background" and "color"
attributes of the "a#register" clause of style.css.

NOTE: This event has been called 'Youth Weekend West' in the past.  There
hasn't been a Youth Weekend East since 2008, so we dropped the "West" part.
