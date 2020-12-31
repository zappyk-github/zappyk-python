#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys, os, io, re

import lib_zappyk._pdf2img2txt
from lib_zappyk._pdf2img2txt import pdf2img2txt

########################################################################################################################
file_name_1 = None
file_name_2 = None
if len(sys.argv) > 1:
    file_name_1 = str(sys.argv[1])
if len(sys.argv) > 2:
    file_name_2 = str(sys.argv[2])
########################################################################################################################
''''
a = {'a' : 0, 'b' : 1}
b = {'c' : 2}
a.update(b)
print(a)

key = 'chiave'

# Changing and adding Dictionary Elements
#my_dict = {'name': 'Jack', 'age': 26}
my_dict = { key: { 0: 'è chiave', 1: 'attributo'} }

# update value
my_dict[key][0] = 'NON è chiave!'
my_dict['age'] = 27

# Output: {'age': 27, 'name': 'Jack'}
print(my_dict)

# add item
my_dict['address'] = 'Downtown'

# Output: {'address': 'Downtown', 'age': 27, 'name': 'Jack'}
print(my_dict)
sys.exit()
'''
########################################################################################################################

p2t_1 = pdf2img2txt(file_name=file_name_1)
fni_1 = p2t_1.make_image()
#fni_1 = p2t_1.make_image(page_save=False)

d_h = 75
# ···················································································································
d_y = 190
coordinate = [1740, d_y, 1760, d_h + 20]  # = Ottobre 2020
p2t_1.make_text_crops('Periodo', coordinate)
# ···················································································································
d_y = 480
coordinate = [280, d_y, 450, d_h]  # = 93517310152
p2t_1.make_text_crops('AziCodFisc', coordinate)

coordinate = [740, d_y, 1600, d_h]  # = HOLLISTER SPA
p2t_1.make_text_crops('AziRagSociale', coordinate)

coordinate = [2490, d_y, 1010, d_h]  # = LBRVLR76S12G812X
p2t_1.make_text_crops('DipCodFisc', coordinate)
# ···················································································································
d_y = 690
coordinate = [280, d_y, 2400, d_h]  # = ALBERTINI VALERIO
p2t_1.make_text_crops('Nominativo', coordinate)

coordinate = [2900, d_y, 600, d_h]  # = 11/12/2015
p2t_1.make_text_crops('DataAssunz', coordinate)
# ···················································································································
d_y = 900
coordinate = [280, d_y, 700, d_h]  # = 000067
p2t_1.make_text_crops('CodAzi', coordinate)

coordinate = [1100, d_y, 700, d_h]  # = 0000071
p2t_1.make_text_crops('Periodo', coordinate)

coordinate = [1980, d_y, 700, d_h]  # = IMP Impiegato
p2t_1.make_text_crops('Qualif', coordinate)

coordinate = [2850, d_y, 650, d_h]  # = 1 1 Livello
p2t_1.make_text_crops('Livello', coordinate)
#_______________________________________________________________________________________________________________________
#
fni_1_pag0 = fni_1[0]

text_crops = p2t_1.read_text_coord(fni_1_pag0, mark_text_coord=True, mark_grid_image=True, save_image=True)

print(text_crops)

########################################################################################################################
sys.exit(0)