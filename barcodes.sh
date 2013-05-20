#!/bin/bash
#Jentak pro inspiraci, prijde mi to elegantnejsi nez ten python... ~harvie

#Rozmery stitku se upravuji tady:
TABLE='-p A4 -t 3x8+10+0-10-0'
MAX=$(( 3*8-1 ))

#Dalsi konfigurace
GEOMETRY=''
ENCTYPE=code128b
PREFIX="$(date +%s)BRM"

barcode -e $ENCTYPE $GEOMETRY $TABLE $(for i in $(seq 0 $MAX); do echo -b $PREFIX$i; done)
