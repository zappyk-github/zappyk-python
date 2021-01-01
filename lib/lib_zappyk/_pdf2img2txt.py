# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os
import cv2
import pytesseract

from pdf2image import convert_from_path

# https://towardsdatascience.com/extracting-text-from-scanned-pdf-using-pytesseract-open-cv-cd670ee38052

def_file_name = None
def_path_work = None
ref_DPI_resolution = 600  # DPI>=300 for best quality
def_DPI_resolution = ref_DPI_resolution
def_CMD_tesseract = '/usr/bin/tesseract'

def_text_crops = {}

def_IMG_extension = 'JPEG'
def_name_image = 'Page_%05i%s.%s'
def_name_work = '-pdf2img2txt'
def_debug = 0

class pdf2img2txt():

    ####################################################################################################################
    def __init__(self, file_name=def_file_name, path_work=def_path_work, DPI_resolution=def_DPI_resolution, CMD_tesseract=def_CMD_tesseract, debug=def_debug):
        if file_name is None:
            raise Exception("Specifica il file PDF da tradurre!")
        if not(os.path.isfile(file_name)):
            raise Exception("Attenzione, il file PDF '%s` non esiste!" % file_name)

        self.debug = debug
        self.file_name = file_name
        self.path_work = path_work
        self.DPI_resolution = DPI_resolution
        self.CMD_tesseract = CMD_tesseract

        self.text_crops = def_text_crops

        if self.path_work is None:
            self.path_work = file_name + def_name_work

        if not(os.path.isdir(self.path_work)):
            os.mkdir(self.path_work)

        #if os.path.isfile(self.CMD_tesseract):
        #    pytesseract.pytesseract.tesseract_cmd = self.CMD_tesseract

    ####################################################################################################################
    def _ratio(self, number):
        number_rate = self.DPI_resolution / ref_DPI_resolution
        number_ratio = int(number * number_rate)

        if self.debug >= 3:
            print("_number_ratio(%10s) >>> %5s >>> (%10s)" % (number, number_rate, number_ratio))

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
    def _make_file_image(self, page_number=0, more_detail=''):
        name_image = def_name_image % (page_number, more_detail, def_IMG_extension)
        file_image = os.path.sep.join((self.path_work, name_image))
        return(file_image)

    ####################################################################################################################
    def _mark_grid_image(self, image_read):
        i = 0
        step = 100
        step_thickness = 1000
        j_vertical = self._ratio(49) * step  # = 4900 |=== 4959 |>>> 2480
        j_horizont = self._ratio(70) * step  # = 7000 |=== 7017 |>>> 3509

        mark_grid_color_j_vertical = (255, 255, 0)
        mark_grid_color_j_horizont = (255, 0, 255)

        mark_grid_thickness_i = 1
        mark_grid_thickness_i_step = 3

        counts = 100
    #CZ#count = [(lambda x: x + 1) for x in range(0, counts, 1)]
    #CZ#for c in count:
        for r in range(0, counts, 1):
            mark_grid_thickness = mark_grid_thickness_i
            if i % step_thickness == 0:
                mark_grid_thickness = mark_grid_thickness_i_step

            if i <= j_vertical:
                image_draw = cv2.line(image_read, (i, 0), (i, j_horizont), color=mark_grid_color_j_vertical, thickness=mark_grid_thickness)
            if i <= j_horizont:
                image_draw = cv2.line(image_read, (0, i), (j_vertical, i), color=mark_grid_color_j_horizont, thickness=mark_grid_thickness)
            i = i + step

        return(image_draw)

    ####################################################################################################################
    def _mark_text_coord(self, image_read, xy0=(), xy1=()):

        mark_text_color = (0, 0, 255)
        mark_text_thickness = 2
        ''''
        for coordinate in coordinates:
            x = coordinate[0]
            y = coordinate[1]
            l = coordinate[2]
            h = coordinate[3]
            (x0, y0, x1, y1) = self._coord_make(x, y, l, h)
        #CZ#image_draw = cv2.rectangle(image_read, (x, y), (x + l, y + h), color=mark_text_color, thickness=mark_text_thickness)
            image_draw = cv2.rectangle(image_read, (x0, y0), (x1, y1), color=mark_text_color, thickness=mark_text_thickness)
        '''
        image_draw = cv2.rectangle(image_read, xy0, xy1, color=mark_text_color, thickness=mark_text_thickness)

        return(image_draw)

    ####################################################################################################################
    def make_image(self, page_save=True):

        file_name_image = []

        pages = convert_from_path(self.file_name, self.DPI_resolution)

        page_number = 1
        for page in pages:
            file_image = self._make_file_image(page_number)
            file_name_image.append(file_image)
            page_number = page_number + 1

            if page_save:
                page.save(file_image, def_IMG_extension)

        return(file_name_image)

    ####################################################################################################################
    def read_text_coord(self, file_image, text_crops={}, page_crops=0, mark_text_coord=False, mark_grid_image=False, save_image=False):
        if not(text_crops):
            text_crops = self.text_crops

        image_read = cv2.imread(file_image)

    #CZ#for page_number in text_crops:
        for page_number in range(page_crops, page_crops+1, 1):
            print("page[%-5s]" % page_number)
            for text_key in text_crops[page_number]:
                coordinate = text_crops[page_number][text_key]['Coordinate']
                x = coordinate[0]
                y = coordinate[1]
                l = coordinate[2]
                h = coordinate[3]
                (x0, y0, x1, y1) = self._coord_make(x, y, l, h)

                # cropping image img = image[y0:y1, x0:x1]
            #CZ#image_crop = image_read[coordinate[0][1]:coordinate[1][1], coordinate[0][0]:coordinate[1][0]]
                image_crop = image_read[y0:y1, x0:x1]

                # convert the image to black and white for better OCR
                (ret, thresh1) = cv2.threshold(image_crop, 120, 255, cv2.THRESH_BINARY)

                # pytesseract image to string to get results
            #CZ#text = str(pytesseract.image_to_string(thresh1, config='--psm 6')
                text = str(pytesseract.image_to_string(thresh1, config='--psm 6', lang='ita'))
               #text = str(pytesseract.image_to_string(thresh1, config='', lang='ita'))
               #text = 'x'

                text_read = text.strip()
                text_crops[page_number][text_key]['TextRead'] = text_read

                if mark_text_coord:
                    image_draw = self._mark_text_coord(image_read, (x0, y0), (x1, y1))

                if self.debug >= 1:
                #CZ#print("page[%-5s]coordinates[%-30s] => key[%-30s] => val[%s]" % (text_page, [(y0,y1), (x0,x1)], text_crop['Key'], text_crop['Val']))
                #CZ#print("page[%-5s] coordinates[%-30s] => key[%-30s] => val[%s]" % (text_page, coordinate, text_crop['Key'], text_crop['Val']))
                #CZ#print("page[%-5s] coordinates[%-30s] => key[%-30s] => val[%s]" % (text_page, coordinate, text_key, text_read))
                    print("page[%-5s] coord[%-30s] key[%-30s] => val[%s]" % (page_number, coordinate, text_key, text_read))

            if mark_grid_image:
                image_draw = self._mark_grid_image(image_read)

            if save_image and (mark_text_coord or mark_grid_image):
            #CZ#name_image_draw = file_image
                file_image_draw = self._make_file_image(page_number, '_markup')
                cv2.imwrite(file_image_draw, image_draw)

        return(text_crops)

    ####################################################################################################################
    def make_text_crops_page(self, page=0, key=None, coordinate=[], val=''):
    #CZ#coordinate = [ x, y, l, h ]
        if not(key is None):
            if not(page in self.text_crops):
                self.text_crops = { page: {} }

            if not(key in self.text_crops[page]):
                self.text_crops[page][key] = {}

            self.text_crops[page][key] = { 'Coordinate': coordinate, 'TextRead': val }

            if self.debug >= 2:
                print("text_crops[%s]" % self.text_crops)

    ####################################################################################################################
    def make_text_crops_page_ZucchettiCartelinoPresenze(self, set_page=0):
        pag = set_page
        #_______________________________________________________________________________________________________________
        #
        d_h = 76
        #···············································································································
        d_y = 190
        self.make_text_crops_page(pag, 'Periodo'       , [1740, d_y, 1760, d_h +  20])  # = Ottobre 2020
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
        self.make_text_crops_page(pag, 'CodAzi'        , [ 280, d_y,  700, d_h      ])  # = 000067
        self.make_text_crops_page(pag, 'CodDip'        , [1100, d_y,  700, d_h      ])  # = 0000071
        self.make_text_crops_page(pag, 'Qualif'        , [1980, d_y,  700, d_h      ])  # = IMP Impiegato
        self.make_text_crops_page(pag, 'Livello'       , [2850, d_y,  650, d_h      ])  # = 1 1 Livello
        #···············································································································
        add = 7
        row = 31
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
        row = 10
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