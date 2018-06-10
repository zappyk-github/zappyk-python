#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'
########################################################################################################################
import sys, time, re
import openpyxl
########################################################################################################################
def str2num(string):
    try:
        pattern = re.compile('^0')
        if pattern.match(string):
            return(string)
        return(float(string))
    except ValueError:
        return(string)
#=======================================================================================================================
print('Init:')
#=======================================================================================================================
file_input  = 'resources/simple.xlsx'
file_output = 'resources/simple-out.xlsx'
#
workbook = openpyxl.load_workbook(file_input, data_only=True)
#
workbook.active = 0
sheetbook = workbook.active
#
col = 'A'
row = 0
row+= 1; sheetbook[col+str(row)] = str2num('9887.23')
row+= 1; sheetbook[col+str(row)] = str2num('435.34')
row+= 1; sheetbook[col+str(row)] = str2num('5467')
row+= 1; sheetbook[col+str(row)] = str2num('000456')
row+= 1; sheetbook[col+str(row)] = time.strftime("%x")
#
workbook.save(file_output)
#=======================================================================================================================
print('Done!')
########################################################################################################################
sys.exit()
