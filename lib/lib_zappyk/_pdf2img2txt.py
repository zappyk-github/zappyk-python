# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os
import re
import sys
import csv
import cv2
import pytesseract

from pdf2image import convert_from_path

# https://towardsdatascience.com/extracting-text-from-scanned-pdf-using-pytesseract-open-cv-cd670ee38052

def_file_name      = None
def_path_work      = None
ref_DPI_resolution = 600  # DPI>=300 for best quality
def_DPI_resolution = ref_DPI_resolution

def_text_crops = {}
def_text_color = (0, 0, 255)
def_type_color = (0, 255, 0)
chr_type_check = '#'

def_CMD_tesseract  = None
def_tesseract_lang = 'ita'
def_tesseract_conf = '--psm 6'
'''
--psm 4   Assume a single column of text of variable sizes.
--psm 5   Assume a single uniform block of vertically aligned text.
--psm 6   Assume a single uniform block of text.
'''

def_IMG_extension = 'JPEG'
def_name_image    = 'Page_%05i%s.%s'
def_name_work     = '-pdf2img2txt'
def_debug         = 0
def_view          = 0

chr_type_key       = '#'
rex_page_key       = '^K(\d+)\.'
chr_page_key       = '::'
csv_delimiter      = ';'
csv_quotechar      = '"'
csv_quoting        = csv.QUOTE_MINIMAL
csv_lineterminator = os.linesep

class pdf2img2txt():

    ####################################################################################################################
    def __init__(self, file_name=def_file_name, path_work=def_path_work, DPI_resolution=def_DPI_resolution, CMD_tesseract=def_CMD_tesseract, debug=def_debug, view=def_view):
        if file_name is None:
            raise Exception("Specifica il file PDF da tradurre!")
        if not(os.path.isfile(file_name)):
            raise Exception("Attenzione, il file PDF '%s` non esiste!" % file_name)
        #
        self.view = view
        self.debug = debug
        self.file_name = file_name
        self.path_work = path_work
        self.DPI_resolution = DPI_resolution
        self.CMD_tesseract = CMD_tesseract
        #
        self.text_crops = def_text_crops
        self.type_check = chr_type_check
        #
        if self.path_work is None:
            self.path_work = file_name + def_name_work
        if not(os.path.isdir(self.path_work)):
            os.mkdir(self.path_work)
        #
        if not(self.CMD_tesseract is None):
            if os.path.isfile(self.CMD_tesseract):
                pytesseract.pytesseract.tesseract_cmd = self.CMD_tesseract
            else:
                print("File command tesseract not found! (%s)" % self.CMD_tesseract)

    ####################################################################################################################
    def _ratio(self, number):
        number_rate = self.DPI_resolution / ref_DPI_resolution
        number_ratio = int(number * number_rate)
        #
        if self.debug >= 3:
            print("_number_ratio(%10s) >>> %5s >>> (%10s)" % (number, number_rate, number_ratio))
        #
        return (number_ratio)

    ####################################################################################################################
    def _ratio_coord(self, x, y, l, h):
        x = self._ratio(x)
        y = self._ratio(y)
        l = self._ratio(l)
        h = self._ratio(h)
        return(x, y, l, h)

    ####################################################################################################################
    def _coord_make(self, x, y, l, h):
        (x, y, l, h) = self._ratio_coord(x, y, l, h)
        x0 = x
        y0 = y
        x1 = x + l
        y1 = y + h
        return(x0, y0, x1, y1)

    ####################################################################################################################
    def _mark_grid_image(self, image_read):
        i = 0
        step = 100
        step_thickness = 1000
        j_vertical = self._ratio(49) * step  # = 4900 |=== 4959 |>>> 2480
        j_horizont = self._ratio(70) * step  # = 7000 |=== 7017 |>>> 3509
        #
        mark_grid_color_j_vertical = (255, 255, 0)
        mark_grid_color_j_horizont = (255, 0, 255)
        #
        mark_grid_thickness_i = 1
        mark_grid_thickness_i_step = 3
        #
        counts = 100
    #CZ#count = [(lambda x: x + 1) for x in range(0, counts, 1)]
    #CZ#for c in count:
        for r in range(0, counts, 1):
            mark_grid_thickness = mark_grid_thickness_i
            if i % step_thickness == 0:
                mark_grid_thickness = mark_grid_thickness_i_step
            #
            if i <= j_vertical:
                image_draw = cv2.line(image_read, (i, 0), (i, j_horizont), color=mark_grid_color_j_vertical, thickness=mark_grid_thickness)
            if i <= j_horizont:
                image_draw = cv2.line(image_read, (0, i), (j_vertical, i), color=mark_grid_color_j_horizont, thickness=mark_grid_thickness)
            i = i + step
        #
        return(image_draw)

    ####################################################################################################################
    def _mark_text_coord(self, image_read, text_color, xy0=(), xy1=()):
        #
        mark_text_color = text_color
        mark_text_thickness = 2
        #
        image_draw = cv2.rectangle(image_read, xy0, xy1, color=mark_text_color, thickness=mark_text_thickness)
        #
        return(image_draw)

    ####################################################################################################################
    def _make_file_image(self, page_number=0, more_detail=''):
        name_image = def_name_image % (page_number, more_detail, def_IMG_extension)
        file_image = os.path.sep.join((self.path_work, name_image))
        return(file_image)

    ####################################################################################################################
    def make_image(self, page_save=True):
        #
        file_name_image = []
        #
        print("Convert file PDF into image, using %s DPI... (%s)" % (self.DPI_resolution, self.file_name))
        pages = convert_from_path(self.file_name, self.DPI_resolution)
        #
        page_number = 1
        for page in pages:
            file_image = self._make_file_image(page_number)
            file_name_image.append(file_image)
            #
            if page_save:
                print("Write file image %s, page %05d (%s)" % (def_IMG_extension, page_number, file_image))
                page.save(file_image, def_IMG_extension)
            #
            page_number = page_number + 1
        #
        return(file_name_image)

    ####################################################################################################################
    def read_text_coord(self, file_image, text_crops={}, page_crops=0, mark_text_coord=False, mark_grid_image=False, save_image=False, autodetect=False):
        if not(text_crops):
            text_crops = self.text_crops
        #
        image_read = cv2.imread(file_image)
        #
    #CZ#for page_number in text_crops:
        for page_number in range(page_crops, page_crops+1, 1):
            if not(autodetect):
                print("Read elements in file image %s, page %05d... (%s)" % (def_IMG_extension, page_number, file_image))
            #
        #CZ#page_keys = { 0: page_number }
            page_keys = {}
            #
            count_element = 0
            count_elements = 80
            count_elements_dot = '.'
            for text_key in text_crops[page_number]:
                tesseract_lang = text_crops[page_number][text_key]['TesseractLang']
                tesseract_conf = text_crops[page_number][text_key]['TesseractConf']
                text_color     = text_crops[page_number][text_key]['ColorBox']
                coordinate     = text_crops[page_number][text_key]['Coordinate']
                x = coordinate[0]
                y = coordinate[1]
                l = coordinate[2]
                h = coordinate[3]
                (x0, y0, x1, y1) = self._coord_make(x, y, l, h)
                #
                # cropping image img = image[y0:y1, x0:x1]
            #CZ#image_crop = image_read[coordinate[0][1]:coordinate[1][1], coordinate[0][0]:coordinate[1][0]]
                image_crop = image_read[y0:y1, x0:x1]
                #
                # convert the image to black and white for better OCR
                (ret, thresh1) = cv2.threshold(image_crop, 120, 255, cv2.THRESH_BINARY)
                #
                # pytesseract image to string to get results
                text = str(pytesseract.image_to_string(thresh1, lang=tesseract_lang, config=tesseract_conf))
                #
                text_read = text.strip()
                if text_key == self.type_check:
                    text_read_val = text_crops[page_number][text_key]['TextRead']
                    if (text_read_val != text_key) and (text_read_val != text_read):
                        raise Exception("Il file \"%s\" non e' del tipo \"%s\"!" % (file_image, text_read_val))
                text_crops[page_number][text_key]['TextRead'] = text_read
                #
                m = re.search(rex_page_key, text_key)
                if m:
                    i = int(m.group(1))
                    page_keys.update({ i: text_read })
                #
                if mark_text_coord:
                    image_draw = self._mark_text_coord(image_read, text_color, (x0, y0), (x1, y1))
                #
                if not(autodetect):
                    if self.debug >= 1:
                    #CZ#print("page[%-5s]coordinates[%-30s] => key[%-30s] => val[%s]" % (text_page, [(y0,y1), (x0,x1)], text_crop['Key'], text_crop['Val']))
                    #CZ#print("page[%-5s] coordinates[%-30s] => key[%-30s] => val[%s]" % (text_page, coordinate, text_crop['Key'], text_crop['Val']))
                    #CZ#print("page[%-5s] coordinates[%-30s] => key[%-30s] => val[%s]" % (text_page, coordinate, text_key, text_read))
                        print("page[%-5s] coord[%-30s] tesseract[%-3s %-26s] key[%-30s] => val[%s]" % (page_number, coordinate, tesseract_lang, tesseract_conf, text_key, text_read))
                    else:
                        print(count_elements_dot, end='')
                        count_element = count_element + 1
                        if (count_element % count_elements) == 0:
                            print("=%5s elements read" % count_element)
            #
            if not(autodetect):
                if self.debug >= 1:
                    pass
                else:
                    dot4space = count_elements - (count_element % count_elements)
                    dotformat = ' ' * dot4space if dot4space > 0 else ''
                    print("%s=%5s total elements" % (dotformat, count_element))
            #
            for text_key in text_crops[page_number]:
                text_read = text_crops[page_number][text_key]['TextRead']
                page_key = chr_page_key.join(str(x) for x in page_keys.values())
                text_crops[page_number][text_key]['PageKey'] = page_key
                if self.view >= 1:
                    print('|'.join(['', (" %-40s " % page_key), (" %5d " % page_number), (" %-20s " % text_key), (" %30s " % text_read), '']))
            #
            if mark_grid_image:
                image_draw = self._mark_grid_image(image_read)
            #
            if save_image and (mark_text_coord or mark_grid_image):
            #CZ#name_image_draw = file_image
                file_image_draw = self._make_file_image(page_number, '_markup')
                cv2.imwrite(file_image_draw, image_draw)
        #
        return(text_crops)

    ####################################################################################################################
    def save_text_crops_page(self, file_name_csv=None, text_crops={}):
        if not(text_crops):
            text_crops = self.text_crops
        #
        if file_name_csv is None:
            file_out = sys.stdout
        else:
            file_out = open(file_name_csv, mode='w')
        #
        try:
            with file_out as file_csv:
                line_csv = csv.writer(file_csv, delimiter=csv_delimiter, quotechar=csv_quotechar, quoting=csv_quoting, lineterminator=csv_lineterminator)
                #
                for page_number in text_crops:
                    for text_key in text_crops[page_number]:
                        if text_key != self.type_check:
                            text_read = text_crops[page_number][text_key]['TextRead']
                            page_key  = text_crops[page_number][text_key]['PageKey']
                            #
                            line_csv.writerow([page_number, page_key, text_key, text_read])
        finally:
            if file_name_csv is not None:
                print("Write elements in file CSV (%s)" % file_name_csv)
                file_out.close()

    ####################################################################################################################
    def make_text_crops_page(self, pag=0, key=None, coord=[], color=def_text_color, ta_lang=def_tesseract_lang, ta_conf=def_tesseract_conf, val='', pag_key=''):
        #        (x, y) l = length
    #CZ#coord = [ x, y, l, h ]
        #                  h = height
        if not(key is None):
            if not(pag in self.text_crops):
            #CZ#self.text_crops = { pag: {} }
                self.text_crops[pag] = {}
            #
            if not(key in self.text_crops[pag]):
            #CZ#self.text_crops[pag] = { key: {} }
                self.text_crops[pag][key] = {}
            #
            if key == chr_type_check:
                color = def_type_color
            #
            ta_conf = '--dpi %s %s' % (self.DPI_resolution, ta_conf)
            #
            self.text_crops[pag][key] = { 'Coordinate': coord, 'ColorBox': color, 'TesseractLang': ta_lang, 'TesseractConf': ta_conf, 'TextRead': val, 'PageKey': pag_key }
            #
            if self.debug >= 2:
                print("text_crops[%s]" % self.text_crops)

    ####################################################################################################################
    def read_text_coord_autodetect(self, file_image, page_crops=0, mark_text_coord=False, mark_grid_image=False, save_image=False, autodetect=True):
        layout_i = 0
        layout_n = None
        autodetect = True
        #_______________________________________________________________________________________________________________
        #
        r = 3
        for i in range(1, r+1):
            self.text_crops = def_text_crops
            if   i == 1: layout = self.make_text_crops_page_zCartelinoPresenze(page_crops, autodetect)
            elif i == 2: layout = self.make_text_crops_page_zLULCartellinoPresenze(page_crops, autodetect)
            elif i == 3: layout = self.make_text_crops_page_zLULCedolinoPaga(page_crops, autodetect)
        #_______________________________________________________________________________________________________________
        #
            try:
                print("...autodetect (%d)%-30s => " % (i, layout), end='')
                text_read_init = self.text_crops[page_crops][self.type_check]['TextRead']
                text_crops = self.read_text_coord(file_image=file_image, page_crops=page_crops, autodetect=autodetect)
                text_read_done = self.text_crops[page_crops][self.type_check]['TextRead']
                if text_read_init == text_read_done:
                    (layout_i, layout_n) = (i, layout)
                    print("check!")
            except:
                print("no")
                pass
        #_______________________________________________________________________________________________________________
        #
        if layout_i > 0:
            print("Detect %s(%d) :-)" % (layout_n, layout_i))
            #
            self.text_crops = def_text_crops
            if   layout_i == 1: self.make_text_crops_page_zCartelinoPresenze(page_crops)
            elif layout_i == 2: self.make_text_crops_page_zLULCartellinoPresenze(page_crops)
            elif layout_i == 3: self.make_text_crops_page_zLULCedolinoPaga(page_crops)
            self.read_text_coord(file_image=file_image, page_crops=page_crops, mark_text_coord=mark_text_coord, mark_grid_image=mark_grid_image, save_image=save_image)
        else:
            print("Detect nothing! :-(")

    ####################################################################################################################
    def make_text_crops_page_zCartelinoPresenze(self, set_page=0, autodetect=False):
        tag = 'zCartelinoPresenze'
        pag = set_page
        #_______________________________________________________________________________________________________________
        #
    #CZ#self.make_text_crops_page(pag, self.type_check , [470, 185,  920, 101], val=self.type_check)
        self.make_text_crops_page(pag, self.type_check , [470, 185,  920, 101], val='SEZIONE PRESENZE')
        #
        if autodetect: return(tag)
        #_______________________________________________________________________________________________________________
        #
        d_h = 76
        d_y = 190
        self.make_text_crops_page(pag, 'K1.Periodo'    , [1740, d_y, 1760, d_h +  20])  # = Ottobre 2020
        #.··············································································································
        d_y = 480
        self.make_text_crops_page(pag, 'AziCodFisc'    , [ 280, d_y,  450, d_h      ])  # = 93517310152
        self.make_text_crops_page(pag, 'AziRagSociale' , [ 740, d_y, 1600, d_h      ])  # = HOLLISTER SPA
        self.make_text_crops_page(pag, 'DipCodFisc'    , [2490, d_y, 1010, d_h      ])  # = LBRVLR76S12G812X
        #···············································································································
        d_y = 690
        self.make_text_crops_page(pag, 'Nominativo'    , [ 280, d_y, 2400, d_h      ])  # = ALBERTINI VALERIO
        self.make_text_crops_page(pag, 'DataAssunz'    , [2900, d_y,  600, d_h      ])  # = 11/12/2015
        #···············································································································
        d_y = 900
        self.make_text_crops_page(pag, 'K2.CodAzi'     , [ 280, d_y,  700, d_h      ])  # = 000067
        self.make_text_crops_page(pag, 'K3.CodDip'     , [1100, d_y,  700, d_h      ])  # = 0000071
        self.make_text_crops_page(pag, 'Qualif'        , [1980, d_y,  700, d_h      ])  # = IMP Impiegato
        self.make_text_crops_page(pag, 'Livello'       , [2850, d_y,  650, d_h      ])  # = 1 1 Livello
        #···············································································································
        add = 7
        row = 31 ; row = 1
        d_y = 1710
        for gg in range(0, row, 1):
            a_y = gg * d_h + gg * add
            tag = 'gg_%02d_' % (gg + 1)
            self.make_text_crops_page(pag, tag          , [ 200, d_y +a_y,  110, d_h])  # =
            self.make_text_crops_page(pag, tag + 'GSett', [ 320, d_y +a_y,  120, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb1', [ 475, d_y +a_y,  275, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb2', [ 765, d_y +a_y,  285, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb3', [1070, d_y +a_y,  280, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb4', [1365, d_y +a_y,  280, d_h])  # =
            self.make_text_crops_page(pag, tag + 'HOrdi', [1665, d_y +a_y,  160, d_h])  # =
            self.make_text_crops_page(pag, tag + 'HFlex', [1840, d_y +a_y,  160, d_h])  # =
            self.make_text_crops_page(pag, tag + 'HStra', [2012, d_y +a_y,  160, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci1', [2187, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci2', [2512, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci3', [2838, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci4', [3162, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci5', [3487, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci6', [3812, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci7', [4135, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci8', [4460, d_y +a_y,  310, d_h])  # =
        #···············································································································
        d_h = 57
        add = 2
        row = 10 ; row = 1
        d_y = 5570
        for gg in range(0, row, 1):
            a_y = gg * d_h + gg * add
            tag = 'voci_%02d_' % (gg + 1)
            self.make_text_crops_page(pag, tag + '1Cod' , [ 165, d_y +a_y,  180, d_h])  # =
            self.make_text_crops_page(pag, tag + '1Des' , [ 355, d_y +a_y,  730, d_h])  # =
            self.make_text_crops_page(pag, tag + '1Qnt' , [1100, d_y +a_y,  220, d_h])  # =
        #CZ#self.make_text_crops_page(pag, tag + '1TOT' , [ 165, d_y +a_y, 1155, d_h])  # = (not work well)
            self.make_text_crops_page(pag, tag + '2Cod' , [1335, d_y +a_y,  170, d_h])  # =
            self.make_text_crops_page(pag, tag + '2Des' , [1515, d_y +a_y,  730, d_h])  # =
            self.make_text_crops_page(pag, tag + '2Qnt' , [2260, d_y +a_y,  210, d_h])  # =
        #CZ#self.make_text_crops_page(pag, tag + '2TOT' , [1335, d_y +a_y, 1135, d_h])  # = (not work well)
            self.make_text_crops_page(pag, tag + '3Cod' , [2490, d_y +a_y,  170, d_h])  # =
            self.make_text_crops_page(pag, tag + '3Des' , [2670, d_y +a_y,  725, d_h])  # =
            self.make_text_crops_page(pag, tag + '3Qnt' , [3410, d_y +a_y,  210, d_h])  # =
        #CZ#self.make_text_crops_page(pag, tag + '3TOT' , [2490, d_y +a_y, 1130, d_h])  # = (not work well)
            self.make_text_crops_page(pag, tag + '4Cod' , [3640, d_y +a_y,  165, d_h])  # =
            self.make_text_crops_page(pag, tag + '4Des' , [3817, d_y +a_y,  735, d_h])  # =
            self.make_text_crops_page(pag, tag + '4Qnt' , [4560, d_y +a_y,  210, d_h])  # =
        #CZ#self.make_text_crops_page(pag, tag + '4TOT' , [3640, d_y +a_y, 1130, d_h])  # = (not work well)
        #_______________________________________________________________________________________________________________
        #

    ####################################################################################################################
    def make_text_crops_page_zLULCartellinoPresenze(self, set_page=0, autodetect=False):
        tag = 'zLULCartellinoPresenze'
        pag = set_page
        #_______________________________________________________________________________________________________________
        #
    #CZ#self.make_text_crops_page(pag, self.type_check , [273, 2282, 566, 44], ta_conf='--psm 13', val=self.type_check)
        self.make_text_crops_page(pag, self.type_check , [273, 2282, 566, 44], ta_conf='--psm 13', val='PERIODO DI RIFERIMENTO')
        #
        if autodetect: return(tag)
        #_______________________________________________________________________________________________________________
        #
        d_h = 76
        d_y = 190
        self.make_text_crops_page(pag, 'K1.Periodo'    , [1740, d_y, 1760, d_h +  20])  # =
        #.··············································································································
        d_y = 480
        self.make_text_crops_page(pag, 'AziCodFisc'    , [ 280, d_y,  450, d_h      ])  # =
        self.make_text_crops_page(pag, 'AziRagSociale' , [ 740, d_y, 1600, d_h      ])  # =
        self.make_text_crops_page(pag, 'DipCodFisc'    , [2490, d_y, 1010, d_h      ])  # =
        #···············································································································
        d_y = 690
        self.make_text_crops_page(pag, 'Nominativo'    , [ 280, d_y, 2400, d_h      ])  # =
        self.make_text_crops_page(pag, 'DataAssunz'    , [2900, d_y,  600, d_h      ])  # =
        #···············································································································
        d_y = 900
        self.make_text_crops_page(pag, 'K2.CodAzi'     , [ 280, d_y,  700, d_h      ])  # =
        self.make_text_crops_page(pag, 'K3.CodDip'     , [1100, d_y,  700, d_h      ])  # =
        self.make_text_crops_page(pag, 'Qualif'        , [1980, d_y,  700, d_h      ])  # =
        self.make_text_crops_page(pag, 'Livello'       , [2850, d_y,  650, d_h      ])  # =
        #···············································································································
        add = 7
        row = 31 ; row = 1
        d_y = 1710
        for gg in range(0, row, 1):
            a_y = gg * d_h + gg * add
            tag = 'gg_%02d_' % (gg + 1)
            self.make_text_crops_page(pag, tag          , [ 200, d_y +a_y,  110, d_h])  # =
            self.make_text_crops_page(pag, tag + 'GSett', [ 320, d_y +a_y,  120, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb1', [ 475, d_y +a_y,  275, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb2', [ 765, d_y +a_y,  285, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb3', [1070, d_y +a_y,  280, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb4', [1365, d_y +a_y,  280, d_h])  # =
            self.make_text_crops_page(pag, tag + 'HOrdi', [1665, d_y +a_y,  160, d_h])  # =
            self.make_text_crops_page(pag, tag + 'HFlex', [1840, d_y +a_y,  160, d_h])  # =
            self.make_text_crops_page(pag, tag + 'HStra', [2012, d_y +a_y,  160, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci1', [2187, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci2', [2512, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci3', [2838, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci4', [3162, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci5', [3487, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci6', [3812, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci7', [4135, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci8', [4460, d_y +a_y,  310, d_h])  # =
        #_______________________________________________________________________________________________________________
        #

    ####################################################################################################################
    def make_text_crops_page_zLULCedolinoPaga(self, set_page=0, autodetect=False):
        tag = 'zLULCedolinoPaga'
        pag = set_page
        #_______________________________________________________________________________________________________________
        #
    #CZ#self.make_text_crops_page(pag, self.type_check , [3590,  860, 620, 42], ta_conf='--psm 13', val=self.type_check)
        self.make_text_crops_page(pag, self.type_check , [3590,  860, 620, 42], ta_conf='--psm 13', val='PERIODO DI RETRIBUZIONE')
        #
        if autodetect: return(tag)
        #_______________________________________________________________________________________________________________
        #
        d_h = 76
        d_y = 190
        self.make_text_crops_page(pag, 'K1.Periodo'    , [1740, d_y, 1760, d_h +  20])  # =
        #.··············································································································
        d_y = 480
        self.make_text_crops_page(pag, 'AziCodFisc'    , [ 280, d_y,  450, d_h      ])  # =
        self.make_text_crops_page(pag, 'AziRagSociale' , [ 740, d_y, 1600, d_h      ])  # =
        self.make_text_crops_page(pag, 'DipCodFisc'    , [2490, d_y, 1010, d_h      ])  # =
        #···············································································································
        d_y = 690
        self.make_text_crops_page(pag, 'Nominativo'    , [ 280, d_y, 2400, d_h      ])  # =
        self.make_text_crops_page(pag, 'DataAssunz'    , [2900, d_y,  600, d_h      ])  # =
        #···············································································································
        d_y = 900
        self.make_text_crops_page(pag, 'K2.CodAzi'     , [ 280, d_y,  700, d_h      ])  # =
        self.make_text_crops_page(pag, 'K3.CodDip'     , [1100, d_y,  700, d_h      ])  # =
        self.make_text_crops_page(pag, 'Qualif'        , [1980, d_y,  700, d_h      ])  # =
        self.make_text_crops_page(pag, 'Livello'       , [2850, d_y,  650, d_h      ])  # =
        #···············································································································
        add = 7
        row = 31 ; row = 1
        d_y = 1710
        for gg in range(0, row, 1):
            a_y = gg * d_h + gg * add
            tag = 'gg_%02d_' % (gg + 1)
            self.make_text_crops_page(pag, tag          , [ 200, d_y +a_y,  110, d_h])  # =
            self.make_text_crops_page(pag, tag + 'GSett', [ 320, d_y +a_y,  120, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb1', [ 475, d_y +a_y,  275, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb2', [ 765, d_y +a_y,  285, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb3', [1070, d_y +a_y,  280, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb4', [1365, d_y +a_y,  280, d_h])  # =
            self.make_text_crops_page(pag, tag + 'HOrdi', [1665, d_y +a_y,  160, d_h])  # =
            self.make_text_crops_page(pag, tag + 'HFlex', [1840, d_y +a_y,  160, d_h])  # =
            self.make_text_crops_page(pag, tag + 'HStra', [2012, d_y +a_y,  160, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci1', [2187, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci2', [2512, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci3', [2838, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci4', [3162, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci5', [3487, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci6', [3812, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci7', [4135, d_y +a_y,  310, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci8', [4460, d_y +a_y,  310, d_h])  # =
        #_______________________________________________________________________________________________________________
        #