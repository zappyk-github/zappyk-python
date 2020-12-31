# -*- coding: utf-8 -*-
__author__ = 'zappyk'

PROJECT     = 'Pdf2Txt'
DESCRIPTION = 'Turn a PDF file into TXT/CSV file extract text string through coordinate'
VERSION     = (0, 0, 1, 'beta', 1)
VERSION     = '0.1.0.0'

###########################################################
def get_project():
    return(PROJECT)
###########################################################
def get_description():
    return(DESCRIPTION)
###########################################################
#def get_version():
#   return(VERSION)
###########################################################
#def get_version(*arg, **kwargs):
#   from Pdf2Txt.src.version import get_version
#   return(get_version(*arg, **kwargs))
###########################################################
def get_version():
    from Pdf2Txt.src.version import the_version
    return(get_version())
