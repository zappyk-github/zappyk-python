# -*- coding: utf-8 -*-
__author__ = 'zappyk'

PROJECT     = 'XLSx2SplitSheets'
DESCRIPTION = """
It splits a Spreadsheet ( .xls / .xlsx ) in so many files grouped
according to the first N characters of the name of each sheet name.
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
#   from CheckDiskSpace.src.version import get_version
#   return(get_version(*arg, **kwargs))
###########################################################
#def get_version():
#    from CheckDiskSpace.src.version import get_version
#    return(get_version())