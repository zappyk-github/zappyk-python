#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys, re

from lib_zappyk._pdf2txt import _pdf2txt

file_name = None
if len(sys.argv) <= 1:
    print("File PDF?")
    sys.exit(1)
else:
    file_name = str(sys.argv[1])

setup = {}
setup['_Periodo'] = "Y=806|X=210:280"
setup['_CF_Dipe'] = "Y=775|X=300:360"
setup['_Nominat'] = "Y=750|X= 35:150"
setup['_CodAzie'] = "Y=725|X= 35:55 "
setup['_CodDipe'] = "Y=725|X=135:158"
setup['_gg01___'] = "Y=628|X= 30:35 "
setup['_gg02___'] = "Y=618|X= 30:35 "
setup['_gg03___'] = "Y=608|X= 30:35 "
setup['_gg04___'] = "Y=598|X= 30:35 "
setup['_gg05___'] = "Y=588|X= 30:35 "
setup['_gg06___'] = "Y=578|X= 30:35 "
setup['_gg07___'] = "Y=568|X= 30:35 "
setup['_gg08___'] = "Y=558|X= 30:35 "
setup['_gg09___'] = "Y=548|X= 30:35 "
setup['_gg10___'] = "Y=538|X= 30:35 "

sp = '\s*'
dd = sp+'(\d+)'+sp
setup_pattern = "Y="+dd+"\|X="+dd+":"+dd
dv = 1
df = 6

awc = _pdf2txt(file_name)

for i in range(len(awc)):
    page = awc[i]['page']
    xmin = awc[i]['xmin']
    xmax = awc[i]['xmax']
    ymin = awc[i]['ymin']
    ymax = awc[i]['ymax']
    word = awc[i]['word']

    #print(awc[i])
    for e in setup:
        eY    = int(re.search(setup_pattern, setup[e]).group(1))
        eXmin = int(re.search(setup_pattern, setup[e]).group(2))
        eXmax = int(re.search(setup_pattern, setup[e]).group(3))

        cY    = True if ymin >= eY    - dv and ymin <= eY    + dv else False
       #cXmin = True if xmin >= eXmin - dv and xmin <= eXmin + dv else False
        cXmin = True if xmin >= eXmin - df                        else False
        cXmax = True if xmax <= eXmax + df                        else False

        #print("")
        #print("[ %5s | %s:%s | %s:%s ] = [%s]" % (page, xmin, xmax, ymin, ymax, word))
        #print("  %5s [ %s:%s - %s | %s:%s ] => (%s and %s and %s)" % ("", eXmin-dv, eXmin+dv, eXmax+df, eY-dv, eY+dv, cXmin, cXmax, cY))

        if cY and cXmin and cXmax:
            print("# page(%5s) %10s = [%s]" % (page, e, word))

sys.exit(0)