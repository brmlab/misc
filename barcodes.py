#!/usr/bin/python
#
# accept strings on stdin and put them to a SVG in grid layout
# compatible with our sticker papers
#
# example: seq -f %06g 0 1000 | ./barcodes.py
#
# requires zint binary from zint package
#

from subprocess import Popen, PIPE
import sys

svghead = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="1052.3622" height="744.09448" version="1.1" id="svg2" inkscape:version="0.47 r22583" sodipodi:docname="barcodes.svg">
"""

svgfoot = """
</svg>
"""

cntx = 7
cnty = 10
scalex = 1
scaley = 0.8

f = open('barcodes.svg','w')
f.write(svghead)

try:
    for i in range(cntx):
	for j in range(cnty):
	    data = raw_input()
	    elem = Popen(('zint','--directsvg','-d', data), stdout = PIPE).communicate()[0].split('\n')
	    elem = elem[8:-2]
	    elem[0] = elem[0].replace('id="barcode"', 'transform="matrix(%f,0,0,%f,%f,%f)"' % (scalex, scaley, 42+i*150 , 14+j*74.3) )
	    elem[23] = 'brm - ' + elem[23].strip() + ' - lab'
	    f.write('\n'.join(elem))
except EOFError:
    pass

f.write(svgfoot)
f.close()
