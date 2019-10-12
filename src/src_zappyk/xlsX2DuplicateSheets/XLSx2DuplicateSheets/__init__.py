# -*- coding: utf-8 -*-
__author__ = 'zappyk'

PROJECT     = 'XLSx2DuplicateSheets'
DESCRIPTION = """
It duplicate a Spreadsheet ( .xls / .xlsx ) in many workbooks from list
according to the file contain the description of each sheet name.
"""
VERSION     = (0, 1, 0, 'rc'  , 1)
VERSION     = '0.1'

###########################################################
def get_project():
    return(PROJECT)
###########################################################
def get_description():
    return(DESCRIPTION)
###########################################################
def get_version():
    return(VERSION)
###########################################################
#def get_version(*arg, **kwargs):
#   from XLSx2DuplicateSheets.src.version import get_version
#   return(get_version(*arg, **kwargs))
###########################################################
#def get_version():
#    from XLSx2DuplicateSheets.src.version import get_version
#    return(get_version())
