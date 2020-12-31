#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys, os, io, re
########################################################################################################################
file_name_1 = None
file_name_2 = None
if len(sys.argv) > 1:
    file_name_1 = str(sys.argv[1])
if len(sys.argv) > 2:
    file_name_2 = str(sys.argv[2])
#_______________________________________________________________________________________________________________________
#
# pip install pdf2image
#
from pdf2image import convert_from_path

d_resolution = 600
e_resolution = d_resolution
#e_resolution = 800

pdfs = file_name_1
pages = convert_from_path(pdfs, e_resolution)

i = 1
for page in pages:
    image_name = file_name_1 + "_page_" + str(i) + ".jpg"
    page.save(image_name, "JPEG")
    i = i+1
#_______________________________________________________________________________________________________________________
#
# pip install opencv-python
# pip install Pillow
#
import cv2
from PIL import Image


def ratio(on, dr=d_resolution, er=e_resolution):
    r = er / dr
    nn = int(on * r)
    #print("ratio === (%10s) >>> %5s >>> (%10s)" % (on, r, nn))
    return(nn)

def ratio_coord(x, y, l, h, dr=d_resolution, er=e_resolution):
    r = er / dr
    #print("ratio === (%s, %s, %s, %s) >>> %s" % (x, y, l, h, r))
    x = ratio(x, dr, er)
    y = ratio(y, dr, er)
    l = ratio(l, dr, er)
    h = ratio(h, dr, er)
    #print("ratio >>> (%s, %s, %s, %s)" % (x, y, l, h))
    return(x, y, l, h)

def mark_region(image_path):
    im = cv2.imread(image_path)

    #gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray, (9, 9), 0)
    #thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)

    # Dilate to combine adjacent text contours
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    #dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
    #cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    x = 0
    r = 100
    cnts_y = [(lambda x: x + 1) for x in range(r)]

    image = None
    line_items_coordinates = []

    i = 0
    t = 100
    s = 1000
    j1 = ratio(49) * t #= 4900 |=== 4959 |>>> 2480
    j2 = ratio(70) * t #= 7000 |=== 7017 |>>> 3509
    #for c in cnts:
    for y in cnts_y:
        #area = cv2.contourArea(c)
        #(x, y, w, h) = cv2.boundingRect(c)

        f_color_j1 = (255, 255, 0)
        f_color_j2 = (255, 0, 255)
        f_thickness=1
        if i % s == 0:
            thickness = 3
        if i <= j1:
            image = cv2.line(im, (i , 0), (i , j2), color=f_color_j1, thickness=f_thickness)
        if i <= j2:
            image = cv2.line(im, (0,  i), (j1,  i), color=f_color_j2, thickness=f_thickness)
        i = i + t

    d_color = (0, 0, 255)
    d_thickness = 2
    d_h = 75
    #···················································································································
    d_y = 190
    (x, y, l, h) = ratio_coord(1740, d_y, 1760, d_h+20) #= Ottobre 2020
    image = cv2.rectangle(im, (x, y), (x+l, y+h), color=d_color, thickness=d_thickness)
    line_items_coordinates.append([(x, y), (x+l, y+h)])
    #···················································································································
    d_y = 480
    (x, y, l, h) = ratio_coord(280, d_y, 450, d_h) #= 93517310152
    image = cv2.rectangle(im, (x, y), (x+l, y+h), color=d_color, thickness=d_thickness)
    line_items_coordinates.append([(x, y), (x+l, y+h)])

    (x, y, l, h) = ratio_coord(740, d_y, 1600, d_h) #= HOLLISTER SPA
    image = cv2.rectangle(im, (x, y), (x+l, y+h), color=d_color, thickness=d_thickness)
    line_items_coordinates.append([(x, y), (x+l, y+h)])

    (x, y, l, h) = ratio_coord(2490, d_y, 1010, d_h) #= LBRVLR76S12G812X
    image = cv2.rectangle(im, (x, y), (x+l, y+h), color=d_color, thickness=d_thickness)
    line_items_coordinates.append([(x, y), (x+l, y+h)])
    #···················································································································
    d_y = 690
    (x, y, l, h) = ratio_coord(280, d_y, 2400, d_h) #= ALBERTINI VALERIO
    image = cv2.rectangle(im, (x, y), (x+l, y+h), color=d_color, thickness=d_thickness)
    line_items_coordinates.append([(x, y), (x+l, y+h)])

    (x, y, l, h) = ratio_coord(2900, d_y, 600, d_h) #= 11/12/2015
    image = cv2.rectangle(im, (x, y), (x+l, y+h), color=d_color, thickness=d_thickness)
    line_items_coordinates.append([(x, y), (x+l, y+h)])
    #···················································································································
    d_y = 900
    (x, y, l, h) = ratio_coord(280, d_y, 700, d_h) #= 000067
    image = cv2.rectangle(im, (x, y), (x+l, y+h), color=d_color, thickness=d_thickness)
    line_items_coordinates.append([(x, y), (x+l, y+h)])

    (x, y, l, h) = ratio_coord(1100, d_y, 700, d_h) #= 0000071
    image = cv2.rectangle(im, (x, y), (x+l, y+h), color=d_color, thickness=d_thickness)
    line_items_coordinates.append([(x, y), (x+l, y+h)])

    (x, y, l, h) = ratio_coord(1980, d_y, 700, d_h)  #= IMP Impiegato
    image = cv2.rectangle(im, (x, y), (x + l, y + h), color=d_color, thickness=d_thickness)
    line_items_coordinates.append([(x, y), (x + l, y + h)])

    (x, y, l, h) = ratio_coord(2850, d_y, 650, d_h)  #= 1 1 Livello
    image = cv2.rectangle(im, (x, y), (x + l, y + h), color=d_color, thickness=d_thickness)
    line_items_coordinates.append([(x, y), (x + l, y + h)])
    #···················································································································
    cv2.imwrite(image_path + '_rectangle.jpg', image)

    return(image, line_items_coordinates)
#_______________________________________________________________________________________________________________________
#
file_name_1_page_1 = file_name_1 + "_page_" + str(1) + ".jpg"

(image, line_items_coordinates) = mark_region(file_name_1_page_1)

#sys.exit(0)
#_______________________________________________________________________________________________________________________
#
# pip install pytesseract
#
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

#from matplotlib import pyplot as plt

# load the original image
image = cv2.imread(file_name_1_page_1)

# get co-ordinates to crop the image
for c in line_items_coordinates:
    #c = line_items_coordinates[i]

    # cropping image img = image[y0:y1, x0:x1]
    img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]

    #plt.figure(figsize=(10, 10))
    #plt.imshow(img)

    # convert the image to black and white for better OCR
    (ret, thresh1) = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)

    # pytesseract image to string to get results
    text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))
    #print("coordinates[%-30s] => text[%s]" % (c, text.strip()))
    print("coordinates[%-30s] => text[%s]" % ([(c[0][1],c[1][1]), (c[0][0],c[1][0])], text.strip()))
#_______________________________________________________________________________________________________________________
#
sys.exit(0)