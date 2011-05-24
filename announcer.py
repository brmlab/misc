#!/usr/bin/python

import re
import urllib2
import datetime
import time

url = "http://brmlab.cz/_export/raw/event/start"
src = urllib2.urlopen(url)

now = datetime.datetime.now()

lines = []

l2 = []

#print src.readline()

for line in src :
#	print line
	match = re.match(r"  \* [0-9]",line)
	if match is not None:
		lines.append(line)

for line in lines:
	a = re.match(r"  \* (.*?) (.*)", line)
	if a is not None:
		diff = datetime.datetime.strptime(a.group(1),"%d.%m.%Y") - now
		if diff < datetime.timedelta(weeks=1) and diff >= datetime.timedelta(days=0):
			l2.append(line)

for line in l2:
	# event page s popiskem
	a = re.match(r"  \* (.*) \[\[event:(.*)\|(.*)\]\]", line)
	if a is not None:
		print(a.group(1) + " " + a.group(3) + " - " + " http://brmlab.cz/event/" + a.group(2))
		continue

	# event page bez popisku
	a = re.match(r"  \* (.*) \[\[event:(.*)\]\]", line)
	if a is not None:
		print(a.group(1) + " " + "http://brmlab.cz/event/" + a.group(2))
		continue

	# link s popiskem
	a = re.match(r"  \* (.*) \[\[(?<!event)(.*)\|(.*)\]\]", line)
	if a is not None:
		print(a.group(1) + " " + a.group(3) + " - " + a.group(2))
		continue

	# ostatni
	a = re.match(r"  \* (.*)", line)
	if a is not None:
		print(a.group(1))


