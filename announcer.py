#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2
import datetime
import smtplib
from email.mime.text import MIMEText

url = "http://brmlab.cz/_export/raw/event/start"
smtp_server = "localhost"
dest_addr = "announcer-test@kerestes.cz"

src = urllib2.urlopen(url)
now = datetime.datetime.now()

lines = []
l2 = []
out = []

for line in src :
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
		out.append(a.group(1) + " " + a.group(3) + " - " + " http://brmlab.cz/event/" + a.group(2) + "\n")
		continue

	# event page bez popisku
	a = re.match(r"  \* (.*) \[\[event:(.*)\]\]", line)
	if a is not None:
		out.append(a.group(1) + " " + "http://brmlab.cz/event/" + a.group(2) + "\n")
		continue

	# link s popiskem
	a = re.match(r"  \* (.*) \[\[(?<!event)(.*)\|(.*)\]\]", line)
	if a is not None:
		out.append(a.group(1) + " " + a.group(3) + " - " + a.group(2) + "\n")
		continue

	# ostatni
	a = re.match(r"  \* (.*)", line)
	if a is not None:
		out.append(a.group(1) + "\n")

msg = MIMEText("".join(out), _charset="utf-8")
msg['Subject'] = "Týdenní přehled událostí"
msg['From'] = "noreply@brmlab.cz"
msg['To'] = dest_addr

if out.__len__() > 0:
	s = smtplib.SMTP(smtp_server)
	s.sendmail("noreply@brmlab.cz", dest_addr, msg.as_string())
