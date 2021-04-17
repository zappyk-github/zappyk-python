#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import cv2
import numpy as np
import pytesseract
# import imutils

import sys
########################################################################################################################
file_name_IMG = str(sys.argv[1]) if len(sys.argv) > 1 else None
########################################################################################################################

img = cv2.imread(file_name_IMG)
cv2.imshow("original", img)

# turn into gray for next processing
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV * cv2.THRESH_OTSU)[1]
thresh = cv2.bitwise_not(thresh)

# omit the underline
kernel = np.ones((4, 4), np.uint8)
erosion = cv2.erode(thresh, kernel, iterations=1)

# dilate to make the line thicker
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 12))
dilation = cv2.dilate(erosion, kernel, iterations=1)

# find the contour
cntrs = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cntrs = cntrs[0] if len(cntrs) == 2 else cntrs[1]

result = img.copy()
for c in cntrs:
    # for each letter, create red rectangle
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # prepare letter for OCR
    box = thresh[y:y + h - 2, x:x + w]
    box = cv2.bitwise_not(box)
    box = cv2.GaussianBlur(box, (3, 3), 0)

    # retreive the angle. For the meaning of angle, see below
    # https://namkeenman.wordpress.com/2015/12/18/open-cv-determine-angle-of-rotatedrect-minarearect/
    rect = cv2.minAreaRect(c)
    angle = rect[2]

    # put angle below letter
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (x, y+h+20)
    fontScale = 0.6
    fontColor = (255, 0, 0)
    lineType = 2
    cv2.putText(result, str(angle), bottomLeftCornerOfText, font, fontScale, fontColor, lineType)

    # do the OCR
    custom_config = r'-l eng --oem 3 --psm 10'
    text = pytesseract.image_to_string(box, config=custom_config)
    print("Detected :" + text + ", angle: " + str(angle))

cv2.imshow("result", result)

cv2.waitKey(0)
cv2.destroyAllWindows()
