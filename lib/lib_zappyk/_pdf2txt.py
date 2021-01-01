# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os
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

def_file_name = None
def_out_sort = True        # True=sort output coordinates
def_out_version = 2        # 1=out every | 2=out normal
def_max_space_union = 2    # consecutive spaces that will be considered united
def_word_encode = 'utf-8'  # character encoding
def_view = False
def_debug = 0

class pdf2txt():

    ####################################################################################################################
    def __init__(self, file_name=def_file_name, out_sort=def_out_sort, out_version=def_out_version, max_space_union=def_max_space_union, word_encode=def_word_encode, debug=def_debug):
        if file_name is None:
            raise Exception("Specifica il file PDF da tradurre!")
        if not(os.path.isfile(file_name)):
            raise Exception("Attenzione, il file PDF '%s` non esiste!" % file_name)

        self.debug = debug
        self.file_name = file_name
        self.out_sort = out_sort
        self.out_version = out_version
        self.max_space_union = max_space_union
        self.word_encode = word_encode

    ####################################################################################################################
    def _pdf2txt(self, view=def_view):
        awc = []

        # Open a PDF file.
        fp = open(self.file_name, 'rb')

        # Create a PDF parser object associated with the file object.
        pdfparser = PDFParser(fp)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        pdfdocument = PDFDocument(pdfparser)

        # Check if the document allows text extraction. If not, abort.
        if not pdfdocument.is_extractable:
            raise PDFTextExtractionNotAllowed

        # Create a PDF resource manager object that stores shared resources.
        pdfmanager = PDFResourceManager()

        # Create a PDF device object.
        pdfdevice = PDFDevice(pdfmanager)

        # BEGIN LAYOUT ANALYSIS
        # Set parameters for analysis.
        laparams = LAParams()

        # Create a PDF page aggregator object.
        pdfaggregator = PDFPageAggregator(pdfmanager, laparams=laparams)

        # Create a PDF interpreter object.
        pdfinterpreter = PDFPageInterpreter(pdfmanager, pdfaggregator)

        num_pages = 0
        # loop over all pages in the document
        for page in PDFPage.create_pages(pdfdocument):
            num_pages += 1

            # read the page into a layout object
            pdfinterpreter.process_page(page)
            layout = pdfaggregator.get_result()

            # extract text from this object
            lwc = self.__words_coord(self.__parse_obj(layout._objs))

            if self.out_sort:
                lwc = self.__words_coord_list2dict(lwc, self.word_encode)

                # sort extract
                #             -k page -k yminR -k xmin -k xmax
                # sort -t '|' -k 2.1n -k 4.1nr -k 3.1n -k 5.1n
                lwc.sort(key=lambda x: (-x['ymin'], x['xmin'], x['xmax']))

            for i in range(len(lwc)):
                if self.out_sort:
                    lwc[i]['page'] = num_pages
                else:
                    lwc[i][5] = num_pages
                awc.append(lwc[i])

                owc = None
                if self.out_sort:
                    owc = ("pag.sort=|%5s| %7s | %7s | %7s | %7s |=[%s]" % (num_pages,
                                                                            ("%3.3f" % lwc[i]['xmin']),
                                                                            ("%3.3f" % lwc[i]['ymin']),
                                                                            ("%3.3f" % lwc[i]['xmax']),
                                                                            ("%3.3f" % lwc[i]['ymax']),
                                                                            lwc[i]['word']))
                else:
                    owc = ("pag.norm=|%5s| %7s | %7s | %7s | %7s |=[%s]" % (num_pages,
                                                                            lwc[i][1],
                                                                            lwc[i][2],
                                                                            lwc[i][3],
                                                                            lwc[i][4],
                                                                            lwc[i][0].encode(self.word_encode)))

                if view >= 1:
                    print("#%s" % owc)
        return(awc)

    ####################################################################################################################
    def __parse_obj(self, lt_objs):
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
                self.__parse_obj(obj._objs)
        return(words)

    ####################################################################################################################
    def __get_ymax(self, coord):
        # maximxum y-coordinate of a character
        comma = 0
        pos = 0
        for i in coord:
            if (i == ","):
                comma += 1
            if (comma == 3):
                break
            pos += 1
        return(coord[pos+1:])

    ####################################################################################################################
    def __get_ymin(self, coord):
        # minimum y-coordinate of a character
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
        return(coord[comma1:pos-1])

    ####################################################################################################################
    def __get_xmin(self, coord):
        # maximxum x-coordinate of a character
        pos = 0
        for j in coord:
            pos += 1
            if (j == ","):
                break
        return(coord[:pos-1])

    ####################################################################################################################
    def __get_xmax(self, coord):
        # minimum x-coordinate of a character
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
        return(coord[comma1:pos-1])

    ####################################################################################################################
    def __max(self, y):
        # max(y[i]), maximum y coordinate of a word
        max = 0
        for i in range(len(y)):
        #CZ#if (y[i]>max):
            if (float(y[i]) > max):
            #CZ#max = y[i]
                max = float(y[i])
        return(max)

    ####################################################################################################################
    def __words_coord(self, words):
        # separates characters in words and returns a matrix in the format:
        # words_fin[i] = [word, minimum x-coord, minimum y-coord, max x-coord of the last character and maximum value of y in the word]
        y = []
        x = None
        words_fin = []
        word = ""
        cnt_space = 0
        max_space = self.max_space_union
        for i in range(len(words)):
            a = words[i][1]

            if a == " ":
                cnt_space += 1
            else:
                cnt_space = 0

        #CZ#if (a!=" " and a!="\n" and a!='!' and a!="?" and a!='.' and a!="," and a!="(" and a!=")" and a!=":" and a!=" -" and a!=";"):
            if (a != " " and a != "\n"):
                if self.debug == 2:
                    print("#then: [%s] space(%s) word[%s]" % (a, cnt_space, word))

                if (word == ""):
                #CZ#y = []
                    x = self.__get_xmin(words[i][0])
                    y.append(self.__get_ymax(words[i][0]))
                else:
                    y.append(self.__get_ymax(words[i][0]))
                word += words[i][1]
            else:
                if self.debug == 2:
                    print("#else: [%s] space(%s) word[%s]" % (a, cnt_space, word))
                #_______________________________________________________________________________________________________
                if self.out_version == 1:
                    if (word != ""):
                        words_fin.append([word, x, self.__get_ymin(words[i-1][0]), self.__get_xmax(words[i-1][0]), max(y)])
                    #CZ#word = ""
                        if (cnt_space > 0 and cnt_space <= max_space):
                            word += " "
                        else:
                            word = ""
                #_______________________________________________________________________________________________________
                elif self.out_version == 2:
                    if (cnt_space > 0 and cnt_space <= max_space):
                        word += " "
                    if not (cnt_space > 0 and cnt_space <= max_space):
                        if (word != ""):
                            words_fin.append([word, x, self.__get_ymin(words[i - 1][0]), self.__get_xmax(words[i - 1][0]), self.__max(y)])
                            word = ""

        return(words_fin)

    ####################################################################################################################
    def __words_coord_list2dict(self, words, word_encode):
        elements = []
        for i in range(len(words)):
            element = self.__words_coord_array2dict(words[i], word_encode)
            elements.append(element)
        return(elements)
    ####################################################################################################################
    def __words_coord_array2dict(self, word, word_encode):
        element = {}
        element['word'] = str(word[0].encode(word_encode))
        element['xmin'] = float(word[1])
        element['ymin'] = float(word[2])
        element['xmax'] = float(word[3])
        element['ymax'] = float(word[4])
        return(element)