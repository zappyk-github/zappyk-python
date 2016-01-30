# -*- coding: utf-8 -*-
__author__ = 'pes0zap'

PROJECT     = 'TurnReporTxt2Csv'
DESCRIPTION = 'Turn a report in TXT to a CSV file'
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