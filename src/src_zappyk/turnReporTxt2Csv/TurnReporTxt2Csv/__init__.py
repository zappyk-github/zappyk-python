# -*- coding: utf-8 -*-
__author__ = 'zappyk'

PROJECT     = 'TurnReporTxt2Csv'
DESCRIPTION = 'Turn a report in TXT to a CSV/XLS file'
VERSION     = (0, 0, 1, 'beta', 1)
VERSION     = (0, 0, 2, 'beta', 1)
VERSION     = '0.2.0.0'

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
#   from TurnReporTxt2Csv.src.version import get_version
#   return(get_version(*arg, **kwargs))
###########################################################
def get_version():
    from TurnReporTxt2Csv.src.version import the_version
    return(get_version())
