# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import csv
#import xlsxwriter

from tkinter            import *
from tkinter            import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showerror

from lib_zappyk          import _initializeVariable
from lib_zappyk._os_file import _basenameNotExt, _basenameGetExt, _basenameFullPathNotExt, _fileExist
from lib_zappyk._string  import _trim, _trimList, _remove, _search, _findall, _joinSpace, _stringToList, _stringToListOnSpace
from lib_zappyk._pdf2txt import pdf2txt

from Pdf2Txt.cfg.load_cfg    import parser_args, parser_conf, logger_conf
from Pdf2Txt.cfg.load_ini    import *
from Pdf2Txt.src.constants   import *

args = parser_args().args
conf = parser_conf().conf
logs = logger_conf().logs

try:
    out_sort    = conf.get("InputOutput", "out_sort"   , fallback=out_sort)
    out_vers    = conf.get("InputOutput", "out_vers"   , fallback=out_vers)
    max_space   = conf.get("InputOutput", "max_space"  , fallback=max_space)
    word_encode = conf.get("InputOutput", "word_encode", fallback=word_encode)
except:
    pass

out_sort    = args.out_sort    if args.out_sort    is not None else out_sort
out_vers    = args.out_vers    if args.out_vers    is not None else out_vers
max_space   = args.max_space   if args.max_space   is not None else max_space
word_encode = args.word_encode if args.word_encode is not None else word_encode

type_input         = args.type_input
file_input         = args.file_input
file_output        = args.file_output

name_input         = _basenameNotExt(file_input)
exte_output        = _basenameGetExt(file_output)

default_sp = '\s*'
default_dd = default_sp + '(\d+)' + default_sp
default_setup_pattern = "Y=" + default_dd + "\|X=" + default_dd + ":" + default_dd
default_delta_variable = 1
default_delta_fix = 6

if file_input == file_output != CHAR_STD_INOUT:
    logs.error("File input '%s' can't be the same file output!" % file_input)

if args.debug >= 1:
    logs.info('out_sort           = %s' % repr(out_sort))
    logs.info('out_vers           = %s' % repr(out_vers))
    logs.info('max_space          = %s' % repr(max_space))
    logs.info('word_encode        = %s' % repr(word_encode))
    logs.info('type_input         = %s' % repr(type_input))
    logs.info('file_input         = %s' % repr(file_input))
    logs.info('file_output        = %s' % repr(file_output))
    logs.info('--------------------')

###############################################################################
def main():
    (ss, sp, dv, df) = (None, None, None, None)

    if (type_input == TYPE_IN_CartellinoPresenze):
        (ss, sp, dv, df) = setup_Zucchetti_Cartellino_Presenze()

    if (type_input == TYPE_IN_CedolinoPaga):
        (ss, sp, dv, df) = setup_Zucchetti_Cedolino_Paga()

    p2t = pdf2txt(file_name=file_input, out_sort=out_sort, out_version=out_vers, max_space_union=max_space, word_encode=word_encode, debug=args.debug)
#CZ#awc = p2t._pdf2txt(True)
    awc = p2t._pdf2txt()
    lwc = {}

    for i in range(len(awc)):
        page = awc[i]['page']
        xmin = awc[i]['xmin']
        xmax = awc[i]['xmax']
        ymin = awc[i]['ymin']
        ymax = awc[i]['ymax']
        word = awc[i]['word']

        twc = {}
        # print(awc_1[i])
        for e in ss:
            eY    = int(re.search(sp, ss[e]).group(1))
            eXmin = int(re.search(sp, ss[e]).group(2))
            eXmax = int(re.search(sp, ss[e]).group(3))

            cY    = True if ymin >= eY - dv and ymin <= eY + dv else False
        #CZ#cXmin = True if xmin >= eXmin - dv and xmin <= eXmin + dv else False
            cXmin = True if xmin >= eXmin - df else False
            cXmax = True if xmax <= eXmax + df else False

            # print("")
            # print("[ %5s | %s:%s | %s:%s ] = [%s]" % (page, xmin, xmax, ymin, ymax, word))
            # print("  %5s [ %s:%s - %s | %s:%s ] => (%s and %s and %s)" % ("", eXmin-dv, eXmin+dv, eXmax+df, eY-dv, eY+dv, cXmin, cXmax, cY))

            if cY and cXmin and cXmax:
                # print("# page(%5s) %10s = [%s]" % (page, e, word))

                if (type_input == TYPE_IN_CartellinoPresenze):
                    #twc = {'Page': page}
                    if e == '_Periodo': twc = {'PageBody': {'Periodo': word }}
                    if e == '_CF_Dipe': twc = {'PageBody': {'CF_Dipe': word }}
                    if e == '_Nominat': twc = {'PageBody': {'Nominat': word }}

                    #if e == '_gg01___': twc['PageBody']['Giorni_']['gg01'] = word
                    #if e == '_gg02___': twc['PageBody']['Giorni_']['gg02'] = word
                    #if e == '_gg03___': twc['PageBody']['Giorni_']['gg03'] = word
                    #if e == '_gg04___': twc['PageBody']['Giorni_']['gg04'] = word

                    #if e == '_gg01Set': twc['PageBody']['Giorni_']['gs01'] = word
                    #if e == '_gg02Set': twc['PageBody']['Giorni_']['gs02'] = word
                    #if e == '_gg03Set': twc['PageBody']['Giorni_']['gs03'] = word
                    #if e == '_gg04Set': twc['PageBody']['Giorni_']['gs04'] = word

        #print("twc=[%s]" % twc)
        #lwc.update(twc)
        lwc[page] = twc

    print("lwc=[%s]" % lwc)

    sys.exit(0)

###############################################################################
def setup_Zucchetti_Cartellino_Presenze():
    setup_string = {}
    setup_string['_Periodo'] = "Y=806|X=210:280"
    setup_string['_CF_Dipe'] = "Y=775|X=300:360"
    setup_string['_Nominat'] = "Y=750|X= 35:150"
    setup_string['_CodAzie'] = "Y=725|X= 35:55 "
    setup_string['_CodDipe'] = "Y=725|X=135:158"

    setup_string['_gg01___'] = "Y=628|X= 30:35 "; setup_string['_gg01Set'] = "Y=628|X= 44:49 ";
    setup_string['_gg02___'] = "Y=618|X= 30:35 "; setup_string['_gg02Set'] = "Y=618|X= 44:49 ";
    setup_string['_gg03___'] = "Y=608|X= 30:35 "; setup_string['_gg03Set'] = "Y=608|X= 44:49 ";
    setup_string['_gg04___'] = "Y=598|X= 30:35 "; setup_string['_gg04Set'] = "Y=598|X= 44:49 ";
    setup_string['_gg05___'] = "Y=588|X= 30:35 "; setup_string['_gg05Set'] = "Y=588|X= 44:49 ";
    setup_string['_gg06___'] = "Y=578|X= 30:35 "; setup_string['_gg06Set'] = "Y=578|X= 44:49 ";
    setup_string['_gg07___'] = "Y=568|X= 30:35 "; setup_string['_gg07Set'] = "Y=568|X= 44:49 ";
    setup_string['_gg08___'] = "Y=558|X= 30:35 "; setup_string['_gg08Set'] = "Y=558|X= 44:49 ";
    setup_string['_gg09___'] = "Y=548|X= 30:35 "; setup_string['_gg09Set'] = "Y=548|X= 44:49 ";
    setup_string['_gg11___'] = "Y=528|X= 30:35 "; setup_string['_gg11Set'] = "Y=528|X= 44:49 ";
    setup_string['_gg10___'] = "Y=538|X= 30:35 "; setup_string['_gg10Set'] = "Y=538|X= 44:49 ";
    setup_string['_gg12___'] = "Y=518|X= 30:35 "; setup_string['_gg12Set'] = "Y=518|X= 44:49 ";
    setup_string['_gg13___'] = "Y=508|X= 30:35 "; setup_string['_gg13Set'] = "Y=508|X= 44:49 ";
    setup_string['_gg14___'] = "Y=498|X= 30:35 "; setup_string['_gg14Set'] = "Y=498|X= 44:49 ";
    setup_string['_gg15___'] = "Y=488|X= 30:35 "; setup_string['_gg15Set'] = "Y=488|X= 44:49 ";
    setup_string['_gg16___'] = "Y=478|X= 30:35 "; setup_string['_gg16Set'] = "Y=478|X= 44:49 ";
    setup_string['_gg17___'] = "Y=468|X= 30:35 "; setup_string['_gg17Set'] = "Y=468|X= 44:49 ";
    setup_string['_gg18___'] = "Y=458|X= 30:35 "; setup_string['_gg18Set'] = "Y=458|X= 44:49 ";
    setup_string['_gg19___'] = "Y=448|X= 30:35 "; setup_string['_gg19Set'] = "Y=448|X= 44:49 ";
    setup_string['_gg20___'] = "Y=438|X= 30:35 "; setup_string['_gg20Set'] = "Y=438|X= 44:49 ";
    setup_string['_gg21___'] = "Y=428|X= 30:35 "; setup_string['_gg21Set'] = "Y=428|X= 44:49 ";
    setup_string['_gg22___'] = "Y=418|X= 30:35 "; setup_string['_gg22Set'] = "Y=418|X= 44:49 ";
    setup_string['_gg23___'] = "Y=408|X= 30:35 "; setup_string['_gg23Set'] = "Y=408|X= 44:49 ";
    setup_string['_gg24___'] = "Y=398|X= 30:35 "; setup_string['_gg24Set'] = "Y=398|X= 44:49 ";
    setup_string['_gg25___'] = "Y=388|X= 30:35 "; setup_string['_gg25Set'] = "Y=388|X= 44:49 ";
    setup_string['_gg26___'] = "Y=378|X= 30:35 "; setup_string['_gg26Set'] = "Y=378|X= 44:49 ";
    setup_string['_gg27___'] = "Y=368|X= 30:35 "; setup_string['_gg27Set'] = "Y=368|X= 44:49 ";
    setup_string['_gg28___'] = "Y=358|X= 30:35 "; setup_string['_gg28Set'] = "Y=358|X= 44:49 ";
    setup_string['_gg29___'] = "Y=348|X= 30:35 "; setup_string['_gg29Set'] = "Y=348|X= 44:49 ";
    setup_string['_gg30___'] = "Y=338|X= 30:35 "; setup_string['_gg30Set'] = "Y=338|X= 44:49 ";
    setup_string['_gg31___'] = "Y=328|X= 30:35 "; setup_string['_gg31Set'] = "Y=328|X= 44:49 ";

    setup_pattern  = default_setup_pattern
    delta_variable = default_delta_variable
    delta_fix      = default_delta_fix

    return(setup_string, setup_pattern, delta_variable, delta_fix)

###############################################################################
def setup_Zucchetti_Cedolino_Paga():
    setup_string   = {}

    setup_pattern  = default_setup_pattern
    delta_variable = default_delta_variable
    delta_fix      = default_delta_fix

    return (setup_string, setup_pattern, delta_variable, delta_fix)