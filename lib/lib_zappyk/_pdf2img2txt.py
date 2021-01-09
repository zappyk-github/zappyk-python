# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os, re, sys, csv, time
import cv2, pytesseract

from datetime import datetime
from pdf2image import convert_from_path

# https://towardsdatascience.com/extracting-text-from-scanned-pdf-using-pytesseract-open-cv-cd670ee38052

def_debug = 0
def_force = 0
def_view  = 0

def_file_name      = None
def_path_work      = None
ref_DPI_resolution = 600  # DPI>=300 for best quality
def_DPI_resolution = ref_DPI_resolution

fix_emptyvalue = ''
num_counterbox = 80
chr_countersep = '|'
chr_counterkey = '*'
chr_counterdot = '·'
chr_countempty = '_'
chr_countspace = ' '
str_legend_log = ";  legend:  %s key,  %s value,  %s empty" % (chr_counterkey, chr_counterdot, chr_countempty)
def_type_color = (0, 255, 0)
def_text_color = (0, 0, 255)
def_text_crops = {}

def_IMG_extension = 'TIFF'
def_IMG_extension = 'JPEG'
def_name_image    = 'Page_%05i%s.%s'
def_name_work     = '___pdf2img2txt'
def_name_markup   = '___markup'

def_CMD_tesseract       = None
def_tesseract_lang      = 'ita'
def_tesseract_lang      = 'ita+eng'
def_tesseract_conf_set  = '--psm 3'
def_tesseract_conf_base = '--psm 6'
def_tesseract_conf_rwal = '--psm 13'
'''
--psm  0    Orientation and script detection (OSD) only.
--psm  1    Automatic page segmentation with OSD.
--psm  2    Automatic page segmentation, but no OSD, or OCR. (not implemented)
--psm  3    Fully automatic page segmentation, but no OSD. (Default)
--psm  4    Assume a single column of text of variable sizes.
--psm  5    Assume a single uniform block of vertically aligned text.
--psm  6    Assume a single uniform block of text.
--psm  7    Treat the image as a single text line.
--psm  8    Treat the image as a single word.
--psm  9    Treat the image as a single word in a circle.
--psm 10    Treat the image as a single character.
--psm 11    Sparse text. Find as much text as possible in no particular order.
--psm 12    Sparse text with OSD.
--psm 13    Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
'''

chr_newline_CarriageReturn = '\r'
chr_newline_LineFeed       = '\n'
chr_newline_OS_Windows = chr_newline_CarriageReturn + chr_newline_LineFeed
chr_newline_OS_Linux   = chr_newline_LineFeed

chr_file_stdout    = '-'
chr_page_key       = '::'
str_page_key_regex = '^K(\d+)\.'
csv_newline_CR     = '<CR>'
csv_newline_LF     = '<LF>'
csv_delimiter      = ';'
csv_quotechar      = '"'
csv_quoting        = csv.QUOTE_MINIMAL
csv_lineterminator = os.linesep

fix_string_warning ='''\
+-----------+
| ATTENTION : %s
+-----------+\
'''

set_debug_markup_Test     = False
set_debug_markup          = False
set_debug_markup_strregex = 'VoceVariabile_01_Sogg.(IRPEF|INPS)'
set_debug_markup_strregex = 'VoceVariabile_0(3|4)_Sogg.INPS'
set_debug_markup_fontsize = 24
set_debug_markup_fontname = '/usr/share/fonts/google-droid/DroidSansMono.ttf'
set_debug_markup_fontname = '/usr/share/fonts/dejavu/DejaVuSansMono.ttf'
set_debug_markup_imagestr = '/tmp/pdf2img2txt-debug-markup-image-string.jpg'
set_debug_markup_imgetthr = '/tmp/pdf2img2txt-debug-markup-image-getval-thresh.jpg'
set_debug_markup_imgetres = '/tmp/pdf2img2txt-debug-markup-image-getval-result.jpg'
set_debug_markup_delaykey = 10000

########################################################################################################################
########################################################################################################################
def _log(string, end=chr_newline_OS_Linux):
    sys.stdout.write(string + end)
########################################################################################################################
########################################################################################################################
class pdf2img2txt():

    ####################################################################################################################
    def __init__(self, file_name=def_file_name, path_work=def_path_work, DPI_resolution=def_DPI_resolution, CMD_tesseract=def_CMD_tesseract, view=def_view, force=def_force, debug=def_debug):
        #
        if file_name is None:
            raise Exception("Specifica il file PDF da tradurre!")
        if not(os.path.isfile(file_name)):
            raise Exception("Attenzione, il file PDF '%s` non esiste!" % file_name)
        #
        self.view = view
        self.force = force
        self.debug = debug
        self.file_name = file_name
        self.path_work = path_work
        self.DPI_resolution = DPI_resolution
        self.CMD_tesseract = CMD_tesseract
        #
        self.text_crops = def_text_crops
        self.type_check = chr_counterkey
        self.set_layout = None
        #
        self.totcount_page = 0
        self.totcount_item = 0
        self.datetime_init = None
        #
        if self.path_work is None:
            self.path_work = file_name + def_name_work
        if not(os.path.isdir(self.path_work)):
            os.mkdir(self.path_work)
        #
        if not(self.CMD_tesseract is None):
            if os.path.isfile(self.CMD_tesseract):
                pytesseract.pytesseract.tesseract_cmd = self.CMD_tesseract
                _log("File command tesseract set: %s" % pytesseract.pytesseract.tesseract_cmd)
            else:
                _log("File command tesseract not found! (%s)" % self.CMD_tesseract)

    ####################################################################################################################
    def _ratio(self, number):
        number_rate = self.DPI_resolution / ref_DPI_resolution
        number_ratio = int(number * number_rate)
        #
        if self.debug >= 3:
            _log("_number_ratio(%10s) >>> %5s >>> (%10s)" % (number, number_rate, number_ratio))
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
    def _image_markup_debug(self, text_merge):
        #
        # import numpy
        # text_nparr = numpy.fromstring(text_merge, numpy.uint8)
        # text_image = numpy.fromstring(text_merge, numpy.uint8)  # .reshape(h, w, nb_planes)
        # text_image = cv2.imdecode(text_nparr, cv2.IMREAD_COLOR)
        # text_image = numpy.fromstring(text_merge, numpy.uint8).reshape()
        # text_image = numpy.fromstring('1 2', dtype=int, sep=' ')
        # textbase64 = base64.b64decode(text_merge)
        # textbase64 = text_merge
        # text_numpy = numpy.frombuffer(textbase64, dtype=numpy.uint8)
        # text_image = cv2.imdecode(text_numpy, flags=1)
        # return (text_image)
        #________________________________________________________________________________
        #
        from PIL import Image
        from PIL import ImageDraw
        from PIL import ImageFont
        fontsize = set_debug_markup_fontsize
        fontname = set_debug_markup_fontname
        colorText = 'black'
        colorOutline = 'red'
        colorBackground = 'white'
        #
        fontImg = ImageFont.truetype(fontname, fontsize)
    #CZ#testImg = Image.new('RGB', (1, 1))
    #CZ#testDraw = ImageDraw.Draw(testImg)
    #CZ#(width, height) = testDraw.textsize(text_merge, fontImg)
        #
        width = 1000
        height = 100
        image = Image.new('RGB', (width + 1, height + 1), colorBackground)
        image_draw = ImageDraw.Draw(image)
        image_draw.text((2, height / 2), text_merge, fill=colorText, font=fontImg)
        image_draw.rectangle((0, 0, width, height), outline=colorOutline)
        image.save(set_debug_markup_imagestr)
        text_image = cv2.imread(set_debug_markup_imagestr, 0)
        #
        return(text_image)

    ####################################################################################################################
    def _read_markup(self, image_crop, tesseract_lang, tesseract_conf, text_key):
        #
        if set_debug_markup_Test:
            (text, thresh, result) = self._read_markup_Test(image_crop, tesseract_lang, tesseract_conf)
        else:
            (text, thresh, result) = self._read_markup_Good(image_crop, tesseract_lang, tesseract_conf)
        #
        text_strip = text.strip()
        #
        if set_debug_markup:
            if re.search(set_debug_markup_strregex, text_key):
                try:
                    # Convert to images
                    text_merge = "[%s] %s" % (text_strip, text_key)
                    text_image = self._image_markup_debug(text_merge)
                    #
                    cv2.imwrite(set_debug_markup_imgetthr, thresh)
                    cv2.imwrite(set_debug_markup_imgetres, result)
                    #
                    cv2.imshow('markup:', text_image)
                    cv2.imshow('thresh:', thresh)
                    cv2.imshow('result:', result)
                    cv2.waitKey(delay=set_debug_markup_delaykey)
                except:
                    _log("Error on debug markup activate!")
        #
        return(text_strip)

    ####################################################################################################################
    def _read_markup_Good(self, image_crop, tesseract_lang, tesseract_conf):
        #
        # convert the image to black and white for better OCR
        (ret, thresh) = cv2.threshold(image_crop, 120, 255, cv2.THRESH_BINARY)
        #
        blur = cv2.GaussianBlur(thresh, (3, 3), 0)
        result = 255 - blur
        #
        # pytesseract image to string to get results
        text = str(pytesseract.image_to_string(thresh, lang=tesseract_lang, config=tesseract_conf))
        #
        return(text, thresh, result)

    ####################################################################################################################
    def _read_markup_Test(self, image_crop, tesseract_lang, tesseract_conf):
        #
        # convert the image to black and white for better OCR
    #CZ#      thresh  = cv2.threshold(image_crop,   0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
    #CZ#(ret, thresh) = cv2.threshold(image_crop,   0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
        (ret, thresh) = cv2.threshold(image_crop, 120, 255, cv2.THRESH_BINARY)
        #
        blur = cv2.GaussianBlur(thresh, (3, 3), 0)
        result = 255 - blur
        #
        # pytesseract image to string to get results
        text = str(pytesseract.image_to_string(thresh, lang=tesseract_lang, config=tesseract_conf, nice=0, timeout=0))
    #CZ#text = str(pytesseract.image_to_pdf_or_hocr(thresh, lang=tesseract_lang, config=tesseract_conf, nice=0, timeout=0))
        #
        return (text, thresh, result)

    ####################################################################################################################
    def _make_file_image(self, page_number=0, more_detail=fix_emptyvalue):
        name_image = def_name_image % (page_number, more_detail, def_IMG_extension)
        file_image = os.path.sep.join((self.path_work, name_image))
        return(file_image)

    ####################################################################################################################
    def make_image(self, page_save=True):
        #
        file_name_image = []
        #
        _log("Convert file PDF into image, using %s DPI... (%s)" % (self.DPI_resolution, self.file_name))
        pages = convert_from_path(self.file_name, self.DPI_resolution)
        #
        page_number = 1
        for page in pages:
            file_image = self._make_file_image(page_number)
            file_name_image.append(file_image)
            #
            if page_save:
                _log("Write file image %s, page %05d (%s)" % (def_IMG_extension, page_number, file_image))
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
        if self.datetime_init is None:
            self.datetime_init = datetime.now()
        datetime_init = datetime.now()
        #
    #CZ#for page_number in text_crops:
        for page_number in range(page_crops, page_crops+1, 1):
            self.totcount_page = self.totcount_page +1
            #
            if not(autodetect):
                _log("Read elements in file image %s, page %05d... (%s)" % (def_IMG_extension, page_number, file_image))
                datetime_init_pag = datetime.now()
            #
        #CZ#page_keys = { 0: page_number }
            page_keys = {}
            #
            count_element = 0
            count_elements = num_counterbox
            for text_key in text_crops[page_number]['Keys']:
                layout_read    = text_crops[page_number]['Layout']
                tesseract_lang = text_crops[page_number]['Keys'][text_key]['TesseractLang']
                tesseract_conf = text_crops[page_number]['Keys'][text_key]['TesseractConf']
                text_color     = text_crops[page_number]['Keys'][text_key]['ColorBox']
                coordinate     = text_crops[page_number]['Keys'][text_key]['Coordinate']
                x = coordinate[0]
                y = coordinate[1]
                l = coordinate[2]
                h = coordinate[3]
                (x0, y0, x1, y1) = self._coord_make(x, y, l, h)
                #
                # cropping image img = image[y0:y1, x0:x1]
                image_crop = image_read[y0:y1, x0:x1]
                #
                text_read = self._read_markup(image_crop, tesseract_lang, tesseract_conf, text_key)
                #
                if self.debug >= 1:
                        _log(" debug read => [%s][%s][%s]" % (page_number, text_key, text_read))
                #
                text_read_val = text_crops[page_number]['Keys'][text_key]['TextRead']
                if text_key == self.type_check:
                    if (text_read_val != text_key) and (text_read_val != text_read):
                        stradd_exception = fix_emptyvalue
                        if self.view:
                            stradd_exception = "; not references \"%s\" is found! ([%s]=>%s)" % (text_read_val, text_read, file_image)
                        string_exception = fix_string_warning % ("file image %s, page %05d, not appear to be specified type %s%s" % (def_IMG_extension, page_number, layout_read, stradd_exception))
                        if not(autodetect):
                            _log(string_exception)
                            if not(self.force):
                                return
                        else:
                            raise Exception(string_exception)
                if (text_read_val == fix_emptyvalue) and (text_read != fix_emptyvalue):
                    text_crops[page_number]['Keys'][text_key]['TextRead'] = text_read
                #
                match_key_regex = re.search(str_page_key_regex, text_key)
                if match_key_regex:
                    i = int(match_key_regex.group(1))
                    page_keys.update({ i: text_read })
                #
                if mark_text_coord:
                    image_draw = self._mark_text_coord(image_read, text_color, (x0, y0), (x1, y1))
                #
                if not(autodetect):
                    if self.debug >= 1:
                        _log("layout[%-20s] page[%-5s] coord[%-30s] tesseract[%-3s %-26s] key[%-30s] => val[%s]" % (layout_read, page_number, coordinate, tesseract_lang, tesseract_conf, text_key, text_read))
                    else:
                        count_element = count_element + 1
                        #
                        if (count_element == 1) or (((count_element - 1) % count_elements) == 0):
                            _log("%s " % chr_countersep, end='')
                        #
                        if (text_key == self.type_check) or match_key_regex:
                            _log(chr_counterkey, end='')
                        else:
                            if text_read == fix_emptyvalue:
                                _log(chr_countempty, end='')
                            else:
                                _log(chr_counterdot, end='')
                        #
                        if (count_element % count_elements) == 0:
                            _log(" %s= %5s elements read" % (chr_countersep, count_element))
            #
            if not(autodetect):
                if self.debug >= 1:
                    pass
                else:
                    dot4space = count_elements - (count_element % count_elements)
                    dotformat = chr_countspace * dot4space if dot4space > 0 else fix_emptyvalue
                    _log("%s %s= %5s total elements" % (dotformat, chr_countersep, count_element))
                #
                datetime_done = datetime.now()
                delta_seconds = (datetime_done - datetime_init).seconds
                delta_HHMMSS_ = time.strftime('%H:%M:%S', time.gmtime(delta_seconds))
                _log("Read elements %d in %d seconds (%s)%s" % (count_element, delta_seconds, delta_HHMMSS_, str_legend_log))
                self.totcount_item = self.totcount_item + count_element
            #
            for text_key in text_crops[page_number]['Keys']:
                text_read = text_crops[page_number]['Keys'][text_key]['TextRead']
            #CZ#page_key = chr_page_key.join(str(x) for x in sort_keys.values())
                page_key = chr_page_key.join(str(page_keys[x]) for x in sorted(page_keys.keys()))
                text_crops[page_number]['Keys'][text_key]['PageKey'] = page_key
                if self.view >= 1:
                    _log('|'.join([fix_emptyvalue, (" %-40s " % page_key), (" %5d " % page_number), (" %-20s " % text_key), (" %30s " % text_read), fix_emptyvalue]))
            #
            if mark_grid_image:
                image_draw = self._mark_grid_image(image_read)
            #
            if save_image and (mark_text_coord or mark_grid_image):
            #CZ#name_image_draw = file_image
                file_image_draw = self._make_file_image(page_number, def_name_markup)
                cv2.imwrite(file_image_draw, image_draw)
            #
        if not (autodetect):
            datetime_done = datetime.now()
            delta_seconds = (datetime_done - self.datetime_init).seconds
            delta_HHMMSS_ = time.strftime('%H:%M:%S', time.gmtime(delta_seconds))
            _log("Finally read %d pages for %d elements in %d seconds (%s)" % (self.totcount_page, self.totcount_item, delta_seconds, delta_HHMMSS_))
        #
        return(text_crops)

    ####################################################################################################################
    def save_text_crops_page(self, file_name_csv=None, text_crops={}):
        if not(text_crops):
            text_crops = self.text_crops
        #
        set_stdout=True if ((file_name_csv is None) or (file_name_csv == chr_file_stdout)) else False
        #
        if not(set_stdout):
            file_out = open(file_name_csv, mode='w')
        else:
            file_out = sys.stdout
        #
        try:
            with file_out as file_csv:
                line_csv = csv.writer(file_csv, delimiter=csv_delimiter, quotechar=csv_quotechar, quoting=csv_quoting, lineterminator=csv_lineterminator)
                #
                for page_number in text_crops:
                    for text_key in text_crops[page_number]['Keys']:
                        if text_key != self.type_check:
                            layout_read = text_crops[page_number]['Layout']
                            page_key    = text_crops[page_number]['Keys'][text_key]['PageKey']
                            text_read   = text_crops[page_number]['Keys'][text_key]['TextRead']
                            text_write  = text_read.replace(chr_newline_CarriageReturn, csv_newline_CR)\
                                                   .replace(chr_newline_LineFeed      , csv_newline_LF)
                            #
                            line_csv.writerow([layout_read, page_number, page_key, text_key, text_write])
        finally:
            if not(set_stdout):
                _log("Write elements in file CSV (%s)" % file_name_csv)
                file_out.close()

    ####################################################################################################################
    def make_text_crops_page(self, pag=0, key=None, coord=[], color=def_text_color, ta_lang=def_tesseract_lang, ta_conf=def_tesseract_conf_base, val=fix_emptyvalue, pag_key=fix_emptyvalue):
        #        (x, y) l = length
    #CZ#coord = [ x, y, l, h ]
        #                  h = height
        if not(key is None):
            if not(pag in self.text_crops):
            #CZ#self.text_crops = { pag: { 'Layout': self.set_layout, 'Keys': {} } }
                self.text_crops[pag] = { 'Layout': self.set_layout, 'Keys': {} }
            #
            if not(key in self.text_crops[pag]['Keys']):
            #CZ#self.text_crops[pag]['Keys'] = { key: {} }
                self.text_crops[pag]['Keys'][key] = {}
            #
            if key == self.type_check:
                color = def_type_color
            #
            ta_conf = '--dpi %s %s' % (self.DPI_resolution, ta_conf)
            #
            self.text_crops[pag]['Keys'][key] = { 'Coordinate': coord, 'ColorBox': color, 'TesseractLang': ta_lang, 'TesseractConf': ta_conf, 'TextRead': val, 'PageKey': pag_key }
            #
            if self.debug >= 2:
                _log("text_crops[%s]" % self.text_crops)

    ####################################################################################################################
    def read_text_coord_autodetect(self, file_image, page_crops=0, mark_text_coord=False, mark_grid_image=False, save_image=False, autodetect=True):
        layout_i = 0
        layout_n = None
        autodetect = True
        #_______________________________________________________________________________________________________________
        #
        r = 4
        for i in range(1, r+1):
            self.text_crops = def_text_crops
            if   i == 1: self.make_text_crops_page_zCartellinoPresenze(set_page=page_crops, set_autodetect=autodetect)
            elif i == 2: self.make_text_crops_page_zLULCartellinoPresenze(set_page=page_crops, set_autodetect=autodetect)
            elif i == 3: self.make_text_crops_page_zLULCedolinoPaga_v1(set_page=page_crops, set_autodetect=autodetect)
            elif i == 4: self.make_text_crops_page_zLULCedolinoPaga_v2(set_page=page_crops, set_autodetect=autodetect)
            #
            try:
                _log(" -> Autodetect page %05d [%d]%-30s: " % (page_crops, i, self.set_layout), end='')
                #
                text_read_init = self.text_crops[page_crops]['Keys'][self.type_check]['TextRead']
                text_crops = self.read_text_coord(file_image=file_image, page_crops=page_crops, autodetect=autodetect)
                text_read_done = self.text_crops[page_crops]['Keys'][self.type_check]['TextRead']
                #
                if text_read_init == text_read_done:
                    (layout_i, layout_n) = (i, self.set_layout)
                    _log("check!")
            except:
                _log("no")
                pass
        #_______________________________________________________________________________________________________________
        #
        if layout_i > 0:
            _log(" => Detect %s[%d] layout :-)" % (layout_n, layout_i))
            #
            self.text_crops = def_text_crops
            if   layout_i == 1: self.make_text_crops_page_zCartellinoPresenze(set_page=page_crops)
            elif layout_i == 2: self.make_text_crops_page_zLULCartellinoPresenze(set_page=page_crops)
            elif layout_i == 3: self.make_text_crops_page_zLULCedolinoPaga_v1(set_page=page_crops)
            elif layout_i == 4: self.make_text_crops_page_zLULCedolinoPaga_v2(set_page=page_crops)
            self.read_text_coord(file_image=file_image, page_crops=page_crops, mark_text_coord=mark_text_coord, mark_grid_image=mark_grid_image, save_image=save_image)
            self.text_crops[page_crops]['Layout'] = layout_n
        else:
            _log(" => Detect nothing layout set! :-(")

    ####################################################################################################################
    def make_text_crops_page_zCartellinoPresenze(self, tag_page='zCartelinoPresenze', set_page=0, set_autodetect=False):
        tag = tag_page
        pag = set_page
        #_______________________________________________________________________________________________________________
        #
    #CZ#self.make_text_crops_page(pag, self.type_check , [470, 185,  920, 101], val=self.type_check)
        self.make_text_crops_page(pag, self.type_check , [470, 185,  920, 101], val='SEZIONE PRESENZE')
        #
        self.set_layout = tag
        if set_autodetect: return
        #_______________________________________________________________________________________________________________
        #
        d_h = 76
        d_y = 190
        self.make_text_crops_page(pag, 'K1.Periodo'    , [1740, d_y, 1760, d_h +  20])  # =
        #···············································································································
        d_y = 480
        self.make_text_crops_page(pag, 'AziCodFisc'    , [ 280, d_y,  450, d_h      ])  # =
        self.make_text_crops_page(pag, 'AziRagSociale' , [ 740, d_y, 1600, d_h      ])  # =
        self.make_text_crops_page(pag, 'DipCodFisc'    , [2490, d_y, 1010, d_h      ])  # =
        #···············································································································
        d_y = 690
        self.make_text_crops_page(pag, 'Nominativo'    , [ 280, d_y, 2400, d_h      ])  # =
        self.make_text_crops_page(pag, 'DipDataAssunz' , [2900, d_y,  600, d_h      ])  # =
        #···············································································································
        d_y = 900
        self.make_text_crops_page(pag, 'K2.CodAzi'     , [ 280, d_y,  700, d_h      ])  # =
        self.make_text_crops_page(pag, 'K3.CodDip'     , [1100, d_y,  700, d_h      ])  # =
        self.make_text_crops_page(pag, 'DipQualif'     , [1980, d_y,  700, d_h      ])  # =
        self.make_text_crops_page(pag, 'DipLivello'    , [2850, d_y,  650, d_h      ])  # =
        #···············································································································
        box ='GG'
        add = 7
        row = 31 # row = 1
        d_y = 1710
        for gg in range(0, row, 1):
            a_y = gg * d_h + gg * add
            tag = '%s_%02d_' % (box, (gg + 1))
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
        box ='Voci'
        d_h = 57
        add = 2
        row = 10 # row = 1
        d_y = 5570
        for gg in range(0, row, 1):
            a_y = gg * d_h + gg * add
            tag = '%s_%02d_' % (box, (gg + 1))
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
    def make_text_crops_page_zLULCartellinoPresenze(self, tag_page='zLULCartellinoPresenze', set_page=0, set_autodetect=False):
        tag = tag_page
        pag = set_page
        # _______________________________________________________________________________________________________________
        #
    #CZ#self.make_text_crops_page(pag, self.type_check , [273, 2282, 566, 44], ta_conf=def_tesseract_conf_rwal, val=self.type_check)
        self.make_text_crops_page(pag, self.type_check , [273, 2282, 566, 44], ta_conf=def_tesseract_conf_rwal, val='PERIODO DI RIFERIMENTO')
        #
        self.set_layout = tag
        if set_autodetect: return
        #_______________________________________________________________________________________________________________
        #
        self.make_text_crops_page(pag, 'InfoDocumento'  , [3540, 655, 1220, 320 ])  # =
        #···············································································································
        d_h = 76
        d_y = 555
        self.make_text_crops_page(pag, 'AziRagSociale'  , [ 220, d_y, 2000, d_h - 10 ])  # =
        #···············································································································
        d_y = 620
        self.make_text_crops_page(pag, 'AziIndiriz.Via' , [ 220, d_y, 1850, d_h - 10 ])  # =
        self.make_text_crops_page(pag, 'AziIndiriz.Civ' , [2080, d_y, 1000, d_h - 10 ])  # =
        #···············································································································
        d_y = 685
        self.make_text_crops_page(pag, 'AziIndiriz.CAP' , [ 220, d_y,  330, d_h - 10 ])  # =
        self.make_text_crops_page(pag, 'AziIndiriz.Com' , [ 560, d_y, 1150, d_h - 10 ])  #, ta_conf=def_tesseract_conf_set)  # =
        self.make_text_crops_page(pag, 'AziIndiriz.Prv' , [1720, d_y,  150, d_h - 10 ])  # =
        #···············································································································
        self.make_text_crops_page(pag, 'K2.CodAziDipAdd', [2590,1400, 2000, d_h - 10 ])  # =
        self.make_text_crops_page(pag, 'Nominativo'     , [2590,1465, 2000, d_h - 10 ])  # =
        self.make_text_crops_page(pag, 'DipIndirizzo_1' , [2590,1530, 2000, d_h - 10 ])  # =
        self.make_text_crops_page(pag, 'DipIndirizzo_2' , [2590,1595, 2000, d_h - 10 ])  # =
        #···············································································································
        d_y = 2350
        self.make_text_crops_page(pag, 'K1.Periodo'     , [ 250, d_y, 1680, d_h      ])  # =
        self.make_text_crops_page(pag, 'DipCodFisc'     , [1960, d_y,  835, d_h      ])  # =
        self.make_text_crops_page(pag, 'DipPatINAIL'    , [2820, d_y,  630, d_h      ])  # =
        self.make_text_crops_page(pag, 'DipAddInfo'     , [3460, d_y, 1310, d_h      ])  # =
        #···············································································································
        box ='GG'
        add = 22
        row = 31 # row = 1
        d_y = 2635
        for gg in range(0, row, 1):
            a_y = gg * d_h + gg * add
            tag = '%s_%02d_' % (box, (gg + 1))
            self.make_text_crops_page(pag, tag + 'GSett', [ 230, d_y +a_y,  135, d_h])  # =
            self.make_text_crops_page(pag, tag          , [ 375, d_y +a_y,   90, d_h])  # =
            self.make_text_crops_page(pag, tag + 'HOrdi', [ 510, d_y +a_y,  260, d_h])  # =
            self.make_text_crops_page(pag, tag + 'HStra', [ 820, d_y +a_y,  250, d_h])  # =
            #
            self.make_text_crops_page(pag, tag + 'Voci1', [1110, d_y +a_y,  410, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci2', [1550, d_y +a_y,  410, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci3', [2000, d_y +a_y,  410, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci4', [2460, d_y +a_y,  410, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Voci5', [2915, d_y +a_y,  410, d_h])  # =
            #
            self.make_text_crops_page(pag, tag + 'Timb1', [3360, d_y +a_y,  410, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb2', [3810, d_y +a_y,  410, d_h])  # =
            self.make_text_crops_page(pag, tag + 'Timb3', [4255, d_y +a_y,  410, d_h])  # =
        #···············································································································
        box ='Voci'
    #CZ#d_h = 57
        add = 1
        row = 9 # row = 1
        d_y = 6155
        for gg in range(0, row, 1):
            a_y = gg * d_h + gg * add
            tag = '%s_%02d_' % (box, (gg + 1))
            self.make_text_crops_page(pag, tag + '1Cod' , [ 240, d_y +a_y,  215, d_h])  # =
            self.make_text_crops_page(pag, tag + '1Des' , [ 470, d_y +a_y,  850, d_h])  # =
            self.make_text_crops_page(pag, tag + '1Qnt' , [1345, d_y +a_y,  400, d_h])  # =
        #CZ#self.make_text_crops_page(pag, tag + '1TOT' , [ 240, d_y +a_y, 1505, d_h])  # = (not work well)
            self.make_text_crops_page(pag, tag + '2Cod' , [1770, d_y +a_y,  135, d_h])  # =
            self.make_text_crops_page(pag, tag + '2Des' , [1920, d_y +a_y,  905, d_h])  # =
            self.make_text_crops_page(pag, tag + '2Qnt' , [2845, d_y +a_y,  390, d_h])  # =
        #CZ#self.make_text_crops_page(pag, tag + '2TOT' , [1770, d_y +a_y, 1465, d_h])  # = (not work well)
            self.make_text_crops_page(pag, tag + '3Cod' , [3255, d_y +a_y,  145, d_h])  # =
            self.make_text_crops_page(pag, tag + '3Des' , [3415, d_y +a_y,  930, d_h])  # =
            self.make_text_crops_page(pag, tag + '3Qnt' , [4365, d_y +a_y,  400, d_h])  # =
        #CZ#self.make_text_crops_page(pag, tag + '3TOT' , [3255, d_y +a_y, 1510, d_h])  # = (not work well)
        #_______________________________________________________________________________________________________________
        #

    ####################################################################################################################
    def make_text_crops_page_zLULCedolinoPaga_v1(self, tag_page='zLULCedolinoPaga_v1', set_page=0, set_autodetect=False):
        tag = tag_page
        pag = set_page
        #_______________________________________________________________________________________________________________
        #
    #CZ#self.make_text_crops_page(pag, self.type_check , [3590,  860, 620, 42], ta_conf=def_tesseract_conf_rwal, val=self.type_check)
        self.make_text_crops_page(pag, self.type_check , [3590,  860, 620, 42], ta_conf=def_tesseract_conf_rwal, val='PERIODO DI RETRIBUZIONE')
        #
        self.set_layout = tag
        if set_autodetect: return
        #_______________________________________________________________________________________________________________
        #
        self.make_text_crops_page(pag, 'InfoDocumento'  , [3592, 477, 1183, 315 ])  # =
        #···············································································································
        d_h = 76
        d_y = 255
        self.make_text_crops_page(pag, 'K2.CodAzi'      , [ 200, d_y,  250, d_h ])  # =
        self.make_text_crops_page(pag, 'AziRagSociale'  , [ 695, d_y, 2000, d_h ])  # =
        #···············································································································
        d_y = 460
        self.make_text_crops_page(pag, 'AziIndiriz.Via' , [ 200, d_y, 2140, d_h ])  # =
        self.make_text_crops_page(pag, 'AziIndiriz.Civ' , [2350, d_y, 1205, d_h ])  # =
        #···············································································································
        d_y = 537
        self.make_text_crops_page(pag, 'AziIndiriz.CAP' , [ 200, d_y,  350, d_h -19])  # =
        self.make_text_crops_page(pag, 'AziIndiriz.Com' , [ 560, d_y, 1390, d_h -19], ta_conf=def_tesseract_conf_set)  # =
        self.make_text_crops_page(pag, 'AziIndiriz.Prv' , [1960, d_y,  150, d_h -19])  # =
        #···············································································································
        d_y = 666
        self.make_text_crops_page(pag, 'AziCodFisc'     , [ 200, d_y     ,  755, d_h ])  # =
        self.make_text_crops_page(pag, 'AziPosINPS'     , [ 995, d_y     ,  620, d_h ])  # =
        self.make_text_crops_page(pag, 'AziPATInail'    , [1635, d_y     ,  596, d_h ])  # =
        self.make_text_crops_page(pag, 'AziCodUnitLocal', [2610, d_y - 54,  945, d_h ])  # =
        self.make_text_crops_page(pag, 'AziDesUnitLocal', [2255, d_y + 36, 1300, d_h ])  # =
        #···············································································································
        d_y = 820
        self.make_text_crops_page(pag, 'DocLineInfo_1'  , [ 220, d_y, 3330, d_h      ])  # =
        #···············································································································
        d_y = 900
        self.make_text_crops_page(pag, 'DocLineInfo_2'  , [ 220, d_y     , 3330, d_h    ])  # =
        self.make_text_crops_page(pag, 'K1.Periodo'     , [3575, d_y     ,  700, d_h -28])  # =
        self.make_text_crops_page(pag, 'PeriodoPresenze', [3575, d_y + 80,  700, d_h -16])  # =
        #···············································································································
        d_y = 1165
        self.make_text_crops_page(pag, 'K3.CodDip'      , [ 230, d_y,       560, d_h ])  # =
        self.make_text_crops_page(pag, 'Nominativo'     , [ 800, d_y,      2850, d_h ])  # =
        self.make_text_crops_page(pag, 'DipCodFisc'     , [3720, d_y,       720, d_h ])  # =
        self.make_text_crops_page(pag, 'DipMatricola'   , [4450, d_y,       360, d_h ])  # =
        #···············································································································
        d_y = 1385
        self.make_text_crops_page(pag, 'DipDataNascita' , [ 230, d_y     ,  370, d_h ])  # =
        self.make_text_crops_page(pag, 'DipDataAssunz'  , [ 630, d_y     ,  370, d_h ])  # =
        self.make_text_crops_page(pag, 'DipDataCessaz'  , [1015, d_y     ,  370, d_h ])  # =
        self.make_text_crops_page(pag, 'DipQualif'      , [1390, d_y - 50,  790, d_h ])  # =
        self.make_text_crops_page(pag, 'DipLivello'     , [2190, d_y - 50,  710, d_h ])  # =
        self.make_text_crops_page(pag, 'DipInfo_1'      , [2915, d_y - 50,  775, d_h ])  # =
        self.make_text_crops_page(pag, 'DipInfo_2'      , [3715, d_y - 50, 1060, d_h ])  # =
        #···············································································································
        d_y = 1520
        self.make_text_crops_page(pag, 'Contratto'      , [2415, d_y     , 2000, d_h ])  # =
        #···············································································································
        d_y = 1600
        self.make_text_crops_page(pag, 'INPS_Sett'      , [ 215, d_y     ,  200, d_h ])  # =
        self.make_text_crops_page(pag, 'INPS_Giorni'    , [ 440, d_y     ,  190, d_h ])  # =
        self.make_text_crops_page(pag, 'Minimale_Ore'   , [ 650, d_y     ,  170, d_h ])  # =
        self.make_text_crops_page(pag, 'Minimale_GG'    , [ 825, d_y     ,  170, d_h ])  # =
        self.make_text_crops_page(pag, 'Minimale_HH'    , [1010, d_y     ,  150, d_h ])  # =
        self.make_text_crops_page(pag, 'Lavorato_Giorni', [1165, d_y     ,  205, d_h ])  # =
        self.make_text_crops_page(pag, 'Lavorato_OreOrd', [1400, d_y     ,  400, d_h ])  # =
        self.make_text_crops_page(pag, 'Lavorato_OreStr', [1830, d_y     ,  360, d_h ])  # =
        self.make_text_crops_page(pag, 'GG_Detrazioni'  , [2220, d_y     ,  210, d_h ])  # =
        #···············································································································
        box = 'ElementiPaga'
        adj = 10
        hgh = d_h + adj
        len = 670
        s_x = 25
        s_y = 0
        syy = 110
        row = 3 # row = 3
        col = 6 # col = 3
        d_x = 600
        d_y = 1720 - adj
        epn = 0
        for epr in range(0, row, 1):
            for epc in range(0, col, 1):
                a_x = len * (epc+0) + s_x * (epc+0)
                a1y = hgh * (epr+0) + s_y * (epr+0) + syy * (epr+0)
                a2y = hgh * (epr+1) + s_y * (epr+1) + syy * (epr+0)
                epn = epn + 1
                tag = '%s_%02d_' % (box, epn)
                self.make_text_crops_page(pag, tag + 'Des', [ d_x +a_x, d_y +a1y, len, hgh ])  # =
                self.make_text_crops_page(pag, tag + 'Val', [ d_x +a_x, d_y +a2y, len, hgh ])  # =
        #···············································································································
        d_y = 2190
        self.make_text_crops_page(pag, 'DataProsScatto' , [ 320, d_y     ,  270, d_h ])  # =
        #···············································································································
        box = 'VoceVariabile'
        add = 11
        row = 30 # row = 1
        d_y = 2406
        for vv in range(0, row, 1):
            a_y = vv * d_h + vv * add
            tag = '%s_%02d_' % (box, (vv + 1))
            self.make_text_crops_page(pag, tag + 'Sogg.IRPEF' , [ 216, d_y +a_y +10,   35, d_h -40 ], ta_conf="--psm 6 --oem 3")  # =
            self.make_text_crops_page(pag, tag + 'Sogg.INPS'  , [ 265, d_y +a_y +10,   35, d_h -40 ], ta_conf="--psm 6 --oem 3")  # =
            self.make_text_crops_page(pag, tag + 'Descrizione', [ 320, d_y +a_y    , 1600, d_h     ])  # =
            self.make_text_crops_page(pag, tag + 'ImportoBase', [1945, d_y +a_y    ,  700, d_h     ])  # =
            self.make_text_crops_page(pag, tag + 'Riferimento', [2670, d_y +a_y    ,  900, d_h     ])  # =
            self.make_text_crops_page(pag, tag + 'Trattenute' , [3600, d_y +a_y    ,  540, d_h     ])  # =
            self.make_text_crops_page(pag, tag + 'Competenze' , [4170, d_y +a_y    ,  610, d_h     ])  # =
        #···············································································································
        box = 'Conguaglio'
        adj = 0
        hgh = d_h + adj
        lnd = 325
        len = 535
        s_x = 5
        s_y = 15
        syy = 90
        row = 1 # row = 1
        col = 8 # col = 3
        d_x = 550
        d_y = 5110 - adj
        epn = 0
        for xxr in range(0, row, 1):
            for xxc in range(0, col, 1):
                a_x = len * (xxc+0) + s_x * (xxc+0)
                a1y = hgh * (xxr+0) + s_y * (xxr+0) + syy * (xxr+0)
                a2y = hgh * (xxr+1) + s_y * (xxr+1) + syy * (xxr+0)
                a3y = hgh * (xxr+2) + s_y * (xxr+2) + syy * (xxr+0)
                len = lnd if (xxc+1)==col else len
                epn = epn + 1
                if xxc==0:
                    tag = '%s_%s_desc' % (box, '%s')
                #CZ#self.make_text_crops_page(pag, tag % 'Testa', [ 225, d_y +a1y, lnd, hgh ])  # =
                    self.make_text_crops_page(pag, tag % 'Riga1', [ 225, d_y +a2y, lnd, hgh ])  # =
                    self.make_text_crops_page(pag, tag % 'Riga2', [ 225, d_y +a3y, lnd, hgh ])  # =
                tag = '%s_%s_col%d' % (box, '%s', (xxc+1))
                self.make_text_crops_page(pag, tag % 'Testa', [ d_x +a_x, d_y +a1y, len, hgh ])  # =
                self.make_text_crops_page(pag, tag % 'Riga1', [ d_x +a_x, d_y +a2y, len, hgh ])  # =
                self.make_text_crops_page(pag, tag % 'Riga2', [ d_x +a_x, d_y +a3y, len, hgh ])  # =
        #···············································································································
        box = 'Progressivi'
        adj = 0
        hgh = d_h + adj
        lnd = 325
        len = 490
        s_x = 140
        s_y = 20
        syy = 90
        row = 1 # row = 1
        col = 7 # col = 3
        d_x = 615
        d_y = 5405 - adj
        epn = 0
        for xxr in range(0, row, 1):
            for xxc in range(0, col, 1):
                a_x = len * (xxc+0) + s_x * (xxc+0)
                a1y = hgh * (xxr+0) + s_y * (xxr+0) + syy * (xxr+0)
                a2y = hgh * (xxr+1) + s_y * (xxr+1) + syy * (xxr+0)
            #CZ#a3y = hgh * (xxr+2) + s_y * (xxr+2) + syy * (xxr+0)
                len = lnd if (xxc+1)==col else len
                epn = epn + 1
                if xxc==0:
                    tag = '%s_%s_desc' % (box, '%s')
                #CZ#self.make_text_crops_page(pag, tag % 'Testa', [ 225, d_y +a1y, lnd, hgh ])  # =
                    self.make_text_crops_page(pag, tag % 'Riga1', [ 225, d_y +a2y, lnd, hgh ])  # =
            #CZ#    self.make_text_crops_page(pag, tag % 'Riga2', [ 225, d_y +a3y, lnd, hgh ])  # =
                tag = '%s_%s_col%d' % (box, '%s', (xxc+1))
                self.make_text_crops_page(pag, tag % 'Testa', [ d_x +a_x, d_y +a1y, len, hgh ])  # =
                self.make_text_crops_page(pag, tag % 'Riga1', [ d_x +a_x, d_y +a2y, len, hgh ])  # =
            #CZ#self.make_text_crops_page(pag, tag % 'Riga2', [ d_x +a_x, d_y +a3y, len, hgh ])  # =
        #···············································································································
        box = 'TFR'
        adj = 0
        hgh = d_h + adj
        lnd = 140
        len = 630
        s_x = 100
        sxx = 20
        s_y = 10
        syy = 90
        row = 1 # row = 1
        col = 6 # col = 3
        d_x = 415
        d_y = 5615 - adj
        epn = 0
        for xxr in range(0, row, 1):
            for xxc in range(0, col, 1):
                a_x = len * (xxc+0) + s_x * (xxc+0)
                a1y = hgh * (xxr+0) + s_y * (xxr+0) + syy * (xxr+0)
                a2y = hgh * (xxr+1) + s_y * (xxr+1) + syy * (xxr+0)
            #CZ#a3y = hgh * (xxr+2) + s_y * (xxr+2) + syy * (xxr+0)
            #CZ#len = lnd if (xxc+1)==col else len
                a_x = a_x + sxx * (xxc+1-(col-2)) if (xxc+1)>=(col-1) else a_x
                epn = epn + 1
                if xxc==0:
                    tag = '%s_%s_desc' % (box, '%s')
                #CZ#self.make_text_crops_page(pag, tag % 'Testa', [ 225, d_y +a1y, lnd, hgh ])  # =
                    self.make_text_crops_page(pag, tag % 'Riga1', [ 225, d_y +a2y, lnd, hgh ])  # =
            #CZ#    self.make_text_crops_page(pag, tag % 'Riga2', [ 225, d_y +a3y, lnd, hgh ])  # =
                tag = '%s_%s_col%d' % (box, '%s', (xxc+1))
                self.make_text_crops_page(pag, tag % 'Testa', [ d_x +a_x, d_y +a1y, len, hgh ])  # =
                self.make_text_crops_page(pag, tag % 'Riga1', [ d_x +a_x, d_y +a2y, len, hgh ])  # =
            #CZ#self.make_text_crops_page(pag, tag % 'Riga2', [ d_x +a_x, d_y +a3y, len, hgh ])  # =
        #···············································································································
        box = 'Ratei'
        adj = 0
        hgh = d_h + adj
        lnd = 720
        lnu = 320
        len = 530
        s_x = 100 - 95
    #CZ#sxx = 20
        s_y = 10 - 2
        syy = 90
        row = 1 # row = 1
        col = 5 # col = 3
        d_x = 970
        d_y = 5860 - adj
        epn = 0
        for xxr in range(0, row, 1):
            for xxc in range(0, col, 1):
                a_x = len * (xxc+0) + s_x * (xxc+0)
                a1y = hgh * (xxr+0) + s_y * (xxr+0) + syy * (xxr+0)
                a2y = hgh * (xxr+1) + s_y * (xxr+1) + syy * (xxr+0)
                a3y = hgh * (xxr+2) + s_y * (xxr+2) + syy * (xxr+0)
                a4y = hgh * (xxr+3) + s_y * (xxr+3) + syy * (xxr+0)
                a5y = hgh * (xxr+4) + s_y * (xxr+4) + syy * (xxr+0)
            #CZ#len = lnd if (xxc+1)==col else len
                len = lnu if (xxc+1)==col else len
            #CZ#a_x = a_x + sxx * (xxc+1-(col-2)) if (xxc+1)>=(col-1) else a_x
                epn = epn + 1
                if xxc==0:
                    tag = '%s_%s_desc' % (box, '%s')
                #CZ#self.make_text_crops_page(pag, tag % 'Testa', [ 225, d_y +a1y, lnd, hgh ])  # =
                    self.make_text_crops_page(pag, tag % 'Riga1', [ 225, d_y +a2y, lnd, hgh ])  # =
                    self.make_text_crops_page(pag, tag % 'Riga2', [ 225, d_y +a3y, lnd, hgh ])  # =
                    self.make_text_crops_page(pag, tag % 'Riga3', [ 225, d_y +a4y, lnd, hgh ])  # =
                    self.make_text_crops_page(pag, tag % 'Riga4', [ 225, d_y +a5y, lnd, hgh ])  # =
                udm = 'Unità di Misura' if (xxc+1)==col else ''
                tag = '%s_%s_col%d' % (box, '%s', (xxc+1))
                self.make_text_crops_page(pag, tag % 'Testa', [ d_x +a_x, d_y +a1y, len, hgh ], val=udm)  # =
                self.make_text_crops_page(pag, tag % 'Riga1', [ d_x +a_x, d_y +a2y, len, hgh ])  # =
                self.make_text_crops_page(pag, tag % 'Riga2', [ d_x +a_x, d_y +a3y, len, hgh ])  # =
                self.make_text_crops_page(pag, tag % 'Riga3', [ d_x +a_x, d_y +a4y, len, hgh ])  # =
                self.make_text_crops_page(pag, tag % 'Riga4', [ d_x +a_x, d_y +a5y, len, hgh ])  # =
        #···············································································································
        self.make_text_crops_page(pag, 'AssegNuclFamig'  , [  890, 6300,  2525, d_h      ])  # =
        self.make_text_crops_page(pag, 'Comunicazioni'   , [  615, 6400,  2800, d_h +234 ])  # =
        self.make_text_crops_page(pag, 'TotaleCompetenze', [ 4080, 5825,   735, d_h      ])  # =
        self.make_text_crops_page(pag, 'TotaleTrattenute', [ 4080, 5925,   735, d_h      ])  # =
        self.make_text_crops_page(pag, 'Arrotondamento'  , [ 4080, 6020,   735, d_h      ])  # =
        self.make_text_crops_page(pag, 'TotaleNettoMese' , [ 3530, 6165,  1100, d_h + 14 ])  # =
        self.make_text_crops_page(pag, 'CoordinateBanca' , [ 3480, 6340,  1475, d_h +299 ])  # =
        #_______________________________________________________________________________________________________________
        #

    ####################################################################################################################
    def make_text_crops_page_zLULCedolinoPaga_v2(self, tag_page='zLULCedolinoPaga_v2', set_page=0, set_autodetect=False):
        tag = tag_page
        pag = set_page
        # _______________________________________________________________________________________________________________
        #
        self.make_text_crops_page_zLULCedolinoPaga_v1(tag_page=tag, set_page=pag, set_autodetect=set_autodetect)
        # _______________________________________________________________________________________________________________
        #
    #CZ#self.make_text_crops_page(pag, self.type_check , [3610, 812, 615, 45], ta_conf=def_tesseract_conf_rwal, val=self.type_check)
        self.make_text_crops_page(pag, self.type_check , [3610, 812, 615, 45], ta_conf=def_tesseract_conf_rwal, val='PERIODO DI RETRIBUZIONE')
        #
        self.set_layout = tag
        if set_autodetect: return
        #_______________________________________________________________________________________________________________
        #
        d_h = 76
        #···············································································································
        box = 'TFR'
        adj = 0
        hgh = d_h + adj
        lnd = 140
        len = 630
        s_x = 100
        sxx = 20 + 30
        s_y = 10
        syy = 90
        row = 1 # row = 1
        col = 6 # col = 3
        d_x = 415
        d_y = 5615 - adj
        epn = 0
        for xxr in range(0, row, 1):
            for xxc in range(0, col, 1):
                a_x = len * (xxc+0) + s_x * (xxc+0)
                a1y = hgh * (xxr+0) + s_y * (xxr+0) + syy * (xxr+0)
                a2y = hgh * (xxr+1) + s_y * (xxr+1) + syy * (xxr+0)
            #CZ#a3y = hgh * (xxr+2) + s_y * (xxr+2) + syy * (xxr+0)
            #CZ#len = lnd if (xxc+1)==col else len
            #CZ#a_x = a_x + sxx * (xxc+1-(col-2)) if (xxc+1)>=(col-1) else a_x
                a_x = a_x - sxx * (xxc+1-(col-2)) if (xxc+1)==(col-1) else a_x
                a_x = a_x + sxx * (xxc+1-(col-2)) if (xxc+1)==(col-0) else a_x
                epn = epn + 1
                if xxc==0:
                    tag = '%s_%s_desc' % (box, '%s')
                #CZ#self.make_text_crops_page(pag, tag % 'Testa', [ 225, d_y +a1y, lnd, hgh ])  # =
                    self.make_text_crops_page(pag, tag % 'Riga1', [ 225, d_y +a2y, lnd, hgh ])  # =
            #CZ#    self.make_text_crops_page(pag, tag % 'Riga2', [ 225, d_y +a3y, lnd, hgh ])  # =
                tag = '%s_%s_col%d' % (box, '%s', (xxc+1))
                self.make_text_crops_page(pag, tag % 'Testa', [ d_x +a_x, d_y +a1y, len, hgh ])  # =
                self.make_text_crops_page(pag, tag % 'Riga1', [ d_x +a_x, d_y +a2y, len, hgh ])  # =
            #CZ#self.make_text_crops_page(pag, tag % 'Riga2', [ d_x +a_x, d_y +a3y, len, hgh ])  # =
        #···············································································································
        self.make_text_crops_page(pag, 'AssegNuclFamig'  , [  890, 6290,  2525, d_h      ])  # =
        self.make_text_crops_page(pag, 'Comunicazioni'   , [  615, 6390,  2800, d_h +234 ])  # =
        self.make_text_crops_page(pag, 'TotaleCompetenze', [ 4080, 5825,   735, d_h      ])  # =
        self.make_text_crops_page(pag, 'TotaleTrattenute', [ 4080, 5925,   735, d_h      ])  # =
        self.make_text_crops_page(pag, 'Arrotondamento'  , [ 4080, 6000,   735, d_h      ])  # =
        self.make_text_crops_page(pag, 'TotaleNettoMese' , [ 3530, 6165,  1100, d_h + 14 ])  # =
        self.make_text_crops_page(pag, 'CoordinateBanca' , [ 3480, 6320,  1475, d_h +299 ])  # =
        #_______________________________________________________________________________________________________________
        #

########################################################################################################################
########################################################################################################################
if __name__ == "__main__":
    #
    file_name_PDF = str(sys.argv[1]) if len(sys.argv) > 1 else None
    file_name_CSV = str(sys.argv[2]) if len(sys.argv) > 2 else None
    file_type_map = str(sys.argv[3]) if len(sys.argv) > 3 else None
    file_pageonly = str(sys.argv[4]) if len(sys.argv) > 4 else None
    #
    pageonly = []
    if not (file_pageonly is None):
        for p in file_pageonly.split(','):
            pageonly.append(int(p.strip()) - 1)
    #
    p2t = pdf2img2txt(file_name=file_name_PDF, DPI_resolution=600, force=True, debug=0)
    fni = p2t.make_image(page_save=True)
    #
    pages = range(len(fni)) if file_pageonly is None else pageonly
    for p in pages:
        page = p + 1
        #
        if not (file_type_map is None):
            if   file_type_map == "zCartellinoPresenze"   : p2t.make_text_crops_page_zCartellinoPresenze(set_page=page)
            elif file_type_map == "zLULCartellinoPresenze": p2t.make_text_crops_page_zLULCartellinoPresenze(set_page=page)
            elif file_type_map == "zLULCedolinoPaga_v1"   : p2t.make_text_crops_page_zLULCedolinoPaga_v1(set_page=page)
            elif file_type_map == "zLULCedolinoPaga_v2"   : p2t.make_text_crops_page_zLULCedolinoPaga_v2(set_page=page)
            else:
                _log("File type %s not configure! :-|" % file_type_map)
                sys.exit(1)
            text_crops = p2t.read_text_coord(file_image=fni[p], page_crops=page, mark_text_coord=True, mark_grid_image=False, save_image=True)
        else:
            p2t.read_text_coord_autodetect(file_image=fni[p], page_crops=page, mark_text_coord=True, mark_grid_image=False, save_image=True)
    #
    p2t.save_text_crops_page(file_name_csv=file_name_CSV)
    #
    sys.exit(0)
