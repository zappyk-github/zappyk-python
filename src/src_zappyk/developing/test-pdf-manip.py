#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'
########################################################################################################################
import sys, time, re
import pdfminer, PyPDF2, pdftotext
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
file_pdf_input  = 'resources/201912_000192_LUL.pdf'
file_pdf_output = 'resources/201912_000192_LUL_CROP.pdf'
#
debug = True
debug = False
#
line_tag_separate_init = '__________________________________________________'
line_tag_separate_done = '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
#
pdf_input1 = None
with open(file_pdf_input, "rb") as in_f:
    pdf_input1 = pdftotext.PDF(in_f)
#
with open(file_pdf_input, "rb") as in_f:
    pdf_input2  = PyPDF2.PdfFileReader(in_f)
    pdf_output = PyPDF2.PdfFileWriter()

    pdf_blank = None
    pdf_blank_page = None

    page_box = 639
    page_box_add = 0
  # page_box_add = 100
    page_num = pdf_input2.getNumPages()
    print("Read document %s ..." % file_pdf_input)
    print("Document has %s pages." % page_num)

    for i in range(page_num):
        page = pdf_input2.getPage(i)
      # page_content = page.extractText()
      # page_content = page.extractText().encode('utf-8')
        page_content = pdf_input1[i]
        if debug:
            print("Document page %5s" % i)
            print("%s_TEXT_INIT_%s" % (line_tag_separate_init, line_tag_separate_init))
            print(page_content)
            print("%s_TEXT_DONE_%s" % (line_tag_separate_done, line_tag_separate_done))

      # page_crop = True if (i % 2) != 0 else False
        page_crop = True if re.findall(r' Variabili di \d{2}/\d{4}', page_content) else False
        if page_crop:
            page_UpperRight_x = page.mediaBox.getUpperRight_x()
            page_UpperRight_y = page.mediaBox.getUpperRight_y()
          # print("Document page %5s, mediaBox: %s" % (i, page.mediaBox))
            print("Document page %5s, crop box: %s x %s" % (i, page_UpperRight_x, page_UpperRight_y))
            #page.trimBox.lowerLeft = (25, 25)
            #page.trimBox.upperRight = (225, 225)
            #page.cropBox.lowerLeft = (50, 50)
            #page.cropBox.upperRight = (200, 200)
            page.trimBox.lowerLeft  = (0+page_box_add, page_box+page_box_add)
            page.trimBox.upperRight = (page_UpperRight_x, page_UpperRight_y)
            page.cropBox.lowerLeft  = (0, page_box)
            page.cropBox.upperRight = (page_UpperRight_x, page_UpperRight_y)
            '''
            if pdf_blank is None:
                pdf_blank = PyPDF2.PdfFileWriter()
              # pdf_blank.addBlankPage(page_UpperRight_x, page_UpperRight_y)
            if pdf_blank_page is None:
              # pdf_blank_page = pdf_blank.getPage(0)
                pdf_blank_page = pdf_blank.createBlankPage()
            page.mergePage(pdf_blank_page)
            '''
        else:
            print("Document page %5s, not crop!" % (i))
        pdf_output.addPage(page)

    print("Write document %s ..." % file_pdf_output)
    with open(file_pdf_output, "wb") as out_f:
        pdf_output.write(out_f)
#
#=======================================================================================================================
print('Done!')
########################################################################################################################
sys.exit()
