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
def_name_image = 'Page_%05i.%s'
def_name_work = '-pdf2img2txt'
def_debug = 1

class pdf2img2txt():

    ###############################################################################
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

        if os.path.isfile(self.CMD_tesseract):
            pytesseract.pytesseract.tesseract_cmd = self.CMD_tesseract

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
    def make_image(self, page_save=True):

        file_name_image = []

        pages = convert_from_path(self.file_name, self.DPI_resolution)

        page_number = 1
        for page in pages:
            name_image = def_name_image % (page_number, def_IMG_extension)
            file_image = os.path.sep.join((self.path_work, name_image))
            file_name_image.append(file_image)
            page_number = page_number + 1

            if page_save:
                page.save(file_image, def_IMG_extension)

        return(file_name_image)

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
    def make_text_crops(self, key=None, coordinate=[], page=0, val=''):
    #CZ#coordinate = [ x, y, l, h ]
        if key is not None:
            if not(page in self.text_crops):
                self.text_crops = { page: {} }

            if not(key in self.text_crops[page]):
                self.text_crops[page][key] = {}

            self.text_crops[page][key] = { 'Coordinate': coordinate, 'TextRead': val }

            if self.debug >= 2:
                print("text_crops[%s]" % self.text_crops)

    ####################################################################################################################
    def read_text_coord(self, file_image, text_crops={}, mark_text_coord=False, mark_grid_image=False, save_image=False):
        if not(text_crops):
            text_crops = self.text_crops
        #text_crops = self.text_crops

        image_read = cv2.imread(file_image)

        for text_page in text_crops:
            for text_key in text_crops[text_page]:
                coordinate = text_crops[text_page][text_key]['Coordinate']
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
                text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))

                text_read = text.strip()
                text_crops[text_page][text_key]['TextRead'] = text_read

                if mark_text_coord:
                    image_draw = self._mark_text_coord(image_read, (x0, y0), (x1, y1))

                if self.debug >= 1:
                #CZ#print("page[%-5s]coordinates[%-30s] => key[%-30s] => val[%s]" % (text_page, [(y0,y1), (x0,x1)], text_crop['Key'], text_crop['Val']))
                #CZ#print("page[%-5s] coordinates[%-30s] => key[%-30s] => val[%s]" % (text_page, coordinate, text_crop['Key'], text_crop['Val']))
                #CZ#print("page[%-5s] coordinates[%-30s] => key[%-30s] => val[%s]" % (text_page, coordinate, text_key, text_read))
                    print("page[%-5s] coord[%-30s] key[%-30s] => val[%s]" % (text_page, coordinate, text_key, text_read))

        if mark_grid_image:
            image_draw = self._mark_grid_image(image_read)

        if save_image and (mark_text_coord or mark_grid_image):
            cv2.imwrite(file_image, image_draw)

        return(text_crops)