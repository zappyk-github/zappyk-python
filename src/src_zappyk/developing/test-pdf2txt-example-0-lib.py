#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys, re

from lib_zappyk._pdf2txt import pdf2txt

file_name_1 = None
file_name_2 = None
if len(sys.argv) > 1:
    file_name_1 = str(sys.argv[1])
if len(sys.argv) > 2:
    file_name_2 = str(sys.argv[2])

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
setup['_gg11___'] = "Y=528|X= 30:35 "
setup['_gg12___'] = "Y=518|X= 30:35 "
setup['_gg13___'] = "Y=508|X= 30:35 "
setup['_gg14___'] = "Y=498|X= 30:35 "
setup['_gg15___'] = "Y=488|X= 30:35 "
setup['_gg16___'] = "Y=478|X= 30:35 "
setup['_gg17___'] = "Y=468|X= 30:35 "
setup['_gg18___'] = "Y=458|X= 30:35 "
setup['_gg19___'] = "Y=448|X= 30:35 "
setup['_gg20___'] = "Y=438|X= 30:35 "
setup['_gg21___'] = "Y=428|X= 30:35 "
setup['_gg22___'] = "Y=418|X= 30:35 "
setup['_gg23___'] = "Y=408|X= 30:35 "
setup['_gg24___'] = "Y=398|X= 30:35 "
setup['_gg25___'] = "Y=388|X= 30:35 "
setup['_gg26___'] = "Y=378|X= 30:35 "
setup['_gg27___'] = "Y=368|X= 30:35 "
setup['_gg28___'] = "Y=358|X= 30:35 "
setup['_gg29___'] = "Y=348|X= 30:35 "
setup['_gg30___'] = "Y=338|X= 30:35 "
setup['_gg31___'] = "Y=328|X= 30:35 "

sp = '\s*'
dd = sp+'(\d+)'+sp
setup_pattern = "Y="+dd+"\|X="+dd+":"+dd
dv = 1
df = 6

p2t_1 = pdf2txt(file_name=file_name_1)
awc_1 = p2t_1._pdf2txt()

#p2t_2 = pdf2Txt(file_name=file_name_2)
#awc_2 = p2t_2._pdf2txt()

for i in range(len(awc_1)):
    page = awc_1[i]['page']
    xmin = awc_1[i]['xmin']
    xmax = awc_1[i]['xmax']
    ymin = awc_1[i]['ymin']
    ymax = awc_1[i]['ymax']
    word = awc_1[i]['word']

    #print(awc_1[i])
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