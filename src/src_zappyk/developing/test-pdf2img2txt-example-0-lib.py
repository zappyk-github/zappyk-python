#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys

from lib_zappyk._pdf2img2txt import pdf2img2txt

########################################################################################################################
file_name_PDF = str(sys.argv[1]) if len(sys.argv) > 1 else None
file_name_CSV = str(sys.argv[2]) if len(sys.argv) > 2 else None
file_type_map = str(sys.argv[3]) if len(sys.argv) > 3 else None
########################################################################################################################
########################################################################################################################
#_______________________________________________________________________________________________________________________
#
p2t = pdf2img2txt(file_name=file_name_PDF, DPI_resolution=600, debug=0)
fni = p2t.make_image(page_save=True)

pages = len(fni)
pages = 1
for p in range(pages):
    page = p + 1

    if not(file_type_map is None):
        if file_type_map == "zCartelinoPresenze":
            p2t.make_text_crops_page_zCartelinoPresenze(page)
        elif file_type_map == "zLULCartellinoPresenze":
            p2t.make_text_crops_page_zLULCartellinoPresenze(page)
        elif file_type_map == "zLULCedolinoPaga":
            p2t.make_text_crops_page_zLULCedolinoPaga(page)
        else:
            print("File type %s not configure! :-|" % file_type_map)
            sys.exit(1)
        text_crops = p2t.read_text_coord(file_image=fni[p], page_crops=page, mark_text_coord=True, mark_grid_image=False, save_image=True)
    else:
        p2t.read_text_coord_autodetect(file_image=fni[p], page_crops=page, mark_text_coord=True, mark_grid_image=False, save_image=True)

p2t.save_text_crops_page(file_name_csv=file_name_CSV)
#_______________________________________________________________________________________________________________________
#
#print(text_crops)
########################################################################################################################
########################################################################################################################
sys.exit(0)