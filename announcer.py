#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2
import datetime
import smtplib
from email.mime.text import MIMEText

url = "http://brmlab.cz/_export/raw/event/start"
smtp_server = "localhost"
dest = ("announce@brmlab.cz", "brmlab@brmlab.cz")

src = urllib2.urlopen(url)
now = datetime.datetime.now()

lines = []
weeklines = []
out = []

for line in src:
	match = re.match(r"  \* [0-9]",line)
	if match is not None:
		lines.append(line)

for line in lines:
	a = re.match(r"  \* (.*?) (.*)", line)
	if a is not None:
		diff = datetime.datetime.strptime(a.group(1),"%d.%m.%Y") - now
		if diff < datetime.timedelta(weeks=1) and diff >= datetime.timedelta(days=0):
			weeklines.append(line)

for line in weeklines:
	# event page s popiskem
	a = re.match(r"  \* (.*) \[\[event:(.*)\|(.*)\]\]", line)
	if a is not None:
		out.append("%s %s - http://brmlab.cz/event/%s" % (a.group(1), a.group(3), a.group(2)))
		continue

	# event page bez popisku
	a = re.match(r"  \* (.*) \[\[event:(.*)\]\]", line)
	if a is not None:
		out.append("%s - http://brmlab.cz/event/%s" % (a.group(1), a.group(2)))
		continue

	# link s popiskem
	a = re.match(r"  \* (.*) \[\[(?<!event)(.*)\|(.*)\]\]", line)
	if a is not None:
		out.append("%s %s - %s" % (a.group(1), a.group(3), a.group(2)))
		continue

	# ostatni
	a = re.match(r"  \* (.*)", line)
	if a is not None:
		out.append(a.group(1))

if len(out):
	out.insert(0, "")
	out.insert(0, "Events taking place in brmlab this week:")
	out.insert(0, "Udalosti v brmlabu tento tyden:")
	msg = MIMEText("\n".join(out), _charset="utf-8")
	msg['Subject'] = "Tydenni prehled udalosti / Weekly overview of events"
	msg['From'] = "noreply@brmlab.cz"
	msg['To'] = dest_addr
	s = smtplib.SMTP(smtp_server)
	for addr in dest:
		s.sendmail("noreply@brmlab.cz", addr, msg.as_string())
