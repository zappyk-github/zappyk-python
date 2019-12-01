#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'
########################################################################################################################
import sys, time, re
import pdfminer, PyPDF2
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
file_pdf_input  = 'resources/pdf-simple.pdf'
file_pdf_output = 'resources/pdf-simple-out.pdf'
#
with open(file_pdf_input, "rb") as in_f:
    input  = PyPDF2.PdfFileReader(in_f)
    output = PyPDF2.PdfFileWriter()

    page_box = 639
    page_num = input.getNumPages()
    print("Read document %s ..." % file_pdf_input)
    print("Document has %s pages." % page_num)

    for i in range(page_num):
        page = input.getPage(i)
        page_crop = True if (i % 2) != 0 else False
        if page_crop:
            page_UpperRight_x = page.mediaBox.getUpperRight_x()
            page_UpperRight_y = page.mediaBox.getUpperRight_y()
            print("Document page %5s, mediaBox: %s" % (i, page.mediaBox))
            print("Document page %5s, crop box: %s x %s" % (i, page_UpperRight_x, page_UpperRight_y))
            #page.trimBox.lowerLeft = (25, 25)
            #page.trimBox.upperRight = (225, 225)
            #page.cropBox.lowerLeft = (50, 50)
            #page.cropBox.upperRight = (200, 200)
            page.trimBox.lowerLeft  = (0, page_box)
            page.trimBox.upperRight = (page_UpperRight_x, page_UpperRight_y)
            page.cropBox.lowerLeft  = (0, page_box)
            page.cropBox.upperRight = (page_UpperRight_x, page_UpperRight_y)
        else:
            print("Document page %5s, not crop!" % (i))
        output.addPage(page)

    print("Write document %s ..." % file_pdf_output)
    with open(file_pdf_output, "wb") as out_f:
        output.write(out_f)
#
#=======================================================================================================================
print('Done!')
########################################################################################################################
sys.exit()
