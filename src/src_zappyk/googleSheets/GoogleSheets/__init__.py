# -*- coding: utf-8 -*-
__author__ = 'pes0zap'

PROJECT     = 'GoogleSheets'
DESCRIPTION = 'Manage your Google Spreadsheets'
VERSION     = (0, 0, 1, 'beta', 1)

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
#   from GoogleSheets.src.version import get_version
#   return(get_version(*arg, **kwargs))
###########################################################
def get_version():
    from GoogleSheets.src.version import get_version
    return(get_version())