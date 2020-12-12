#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys
import pdfminer
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfdocument import PDFDocument

program = str(sys.argv[0])
file_name = None
def_debug = 0
out_sort = True
out_version = 2 # 1=out every | 2=out normal
max_space_union = 2
add_file_name = "_coord.txt"

debug = def_debug
if len(sys.argv) > 1:
    file_name = str(sys.argv[1])
else:
    print("File PDF?")
    sys.exit(1)
if len(sys.argv) > 2:
    debug = int(sys.argv[2])
print("·         program=[%s]" % program)
print("·       file_name=[%s]" % file_name)
print("·           debug=[%s]" % debug)
print("·        out_sort=[%s]" % out_sort)
print("·     out_version=[%s]" % out_version)
print("· max_space_union=[%s]" % max_space_union)

def main():
    # Open a PDF file.
#CZ#name = input("Name of pdf document: ")
    fp = open(file_name, 'rb')

    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Password for initialization as 2nd parameter
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)

    # BEGIN LAYOUT ANALYSIS
    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    file_w=open(file_name + add_file_name, 'w')

    num_pages = 0
    # loop over all pages in the document
    for page in PDFPage.create_pages(document):
        num_pages += 1

        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()

        # extract text from this object
        lwc = words_coord(parse_obj(layout._objs))

        if out_sort:
            lwc = words_coord_list2dict(lwc)

            # sort extract
            lwc.sort(key=lambda x: (-x['ymin'], x['xmin'], x['xmax']))

            for i in range(len(lwc)):
                owc = ("pag.sort=|%5s| %7s | %7s | %7s | %7s |=[%s]" % (num_pages, ("%3.3f" % lwc[i]['xmin']), ("%3.3f" % lwc[i]['ymin']), ("%3.3f" % lwc[i]['xmax']), ("%3.3f" % lwc[i]['ymax']), lwc[i]['word'] ))
                if debug >= 1:
                    print("#%s" % owc)
                file_w.write(owc + '\n')
        else:
            for i in range(len(lwc)):
                '''
                owc=""
                for j in range(len(awc[i])):
                #CZ#b + =a[i][j].encode('utf-8') + " "
                    if (j == 0):
                        owc += str(awc[i][j].encode('utf-8')) + " =>| "
                    else:
                        owc += str(awc[i][j]) + " | "
                '''
                # if sorted:
                #             -k page -k yminR -k xmin -k xmax
                # sort -t '|' -k 2.1n -k 4.1nr -k 3.1n -k 5.1n
                owc = ("pag.norm=|%5s| %7s | %7s | %7s | %7s |=[%s]" % (num_pages, lwc[i][1], lwc[i][2], lwc[i][3], lwc[i][4], lwc[i][0].encode('utf-8')))
                if debug >= 1:
                    print("#%s" % owc)
                file_w.write(owc + '\n')

    file_w.close()

    sys.exit(0)

def parse_obj(lt_objs):
    words = []

    # loop over the object list
    for obj in lt_objs:

        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            """print (obj.bbox[0], obj.bbox[1], obj.bbox[2], obj.bbox[3], obj.get_text().replace('\n', '_'))"""
        #CZ#words=[]
            for line in obj:

                if (isinstance(line, pdfminer.layout.LTTextLineHorizontal)):
                    for char in line:
                        pos=0
                        a=char.__repr__()[8:]
                        for i in range(len(a)):
                            if (a[i]==" "):
                                pos=i
                                break
                        words.append([a[:pos], char.get_text()])

        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs)
    return words

def get_ymax(coord):
    #maximxum y-coordinate of a character
    comma = 0
    pos = 0
    for i in coord:
        if (i == ","):
            comma += 1
        if (comma == 3):
            break
        pos += 1
    return coord[pos+1:]

def get_ymin(coord):
    #minimum y-coordinate of a character
    comma = 0
    comma1 = 0
    pos = 0
    for i in coord:
        pos += 1
        if (i == ","):
            comma += 1
            if (comma == 1):
                comma1 = pos
        if (comma == 2):
            break
    return coord[comma1:pos-1]

def get_xmin(coord):
    #maximxum x-coordinate of a character
    pos = 0
    for j in coord:
        pos += 1
        if (j == ","):
            break
    return coord[:pos-1]

def get_xmax(coord):
    #minimum x-coordinate of a character
    comma = 0
    comma1 = 0
    pos = 0
    for i in coord:
        pos += 1
        if (i == ","):
            comma += 1
            if (comma == 2):
                comma1 = pos
        if (comma == 3):
            break
    return coord[comma1:pos-1]

def max(y):
    #max(y[i]), maximum y coordinate of a word
    max = 0
    for i in range(len(y)):
    #CZ#if (y[i]>max):
        if (float(y[i]) > max):
        #CZ#max = y[i]
            max = float(y[i])
    return max

def words_coord(words):
    #separates characters in words and returns a matrix in the format:
    #words_fin[i] = [word, minimum x-coord, minimum y-coord, max x-coord of the last character and maximum value of y in the word]
    words_fin = []
    word = ""
    cnt_space = 0
    max_space = max_space_union
    for i in range(len(words)):
        a = words[i][1]
        if a == " ":
            cnt_space += 1
        else:
            cnt_space = 0

    #CZ#if (a!=" " and a!="\n" and a!='!' and a!="?" and a!='.' and a!="," and a!="(" and a!=")" and a!=":" and a!=" -" and a!=";"):
        if (a != " " and a != "\n"):
            if debug == 2:
                print("#then: [%s] space(%s) word[%s]" % (a, cnt_space, word))

            if (word == ""):
                y = []
                x = get_xmin(words[i][0])
                y.append(get_ymax(words[i][0]))
            else:
                y.append(get_ymax(words[i][0]))
            word += words[i][1]
        else:
            if debug == 2:
                print("#else: [%s] space(%s) word[%s]" % (a, cnt_space, word))
            #___________________________________________________________________________________________________________
            if out_version == 1:
                if (word != ""):
                    words_fin.append([word, x, get_ymin(words[i-1][0]), get_xmax(words[i-1][0]), max(y)])
                #CZ#word = ""
                    if (cnt_space > 0 and cnt_space <= max_space):
                        word += " "
                    else:
                        word = ""
            #___________________________________________________________________________________________________________
            elif out_version == 2:
                if (cnt_space > 0 and cnt_space <= max_space):
                    word += " "
                if not (cnt_space > 0 and cnt_space <= max_space):
                    if (word != ""):
                        words_fin.append([word, x, get_ymin(words[i - 1][0]), get_xmax(words[i - 1][0]), max(y)])
                        word = ""

    return words_fin

def words_coord_list2dict(words):
    elements = []
    for i in range(len(words)):
        element = {}
        element['word'] = str(words[i][0].encode('utf-8'))
        element['xmin'] = float(words[i][1])
        element['ymin'] = float(words[i][2])
        element['xmax'] = float(words[i][3])
        element['ymax'] = float(words[i][4])
        elements.append(element)
    return elements

main()