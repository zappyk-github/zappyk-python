# -*- coding: utf-8 -*-
__author__ = 'pes0zap'

PROJECT     = 'QueryReporting'
DESCRIPTION = 'Query Reporting management and output CSV/XLS file'
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
#   from QueryReporting.src.version import get_version
#   return(get_version(*arg, **kwargs))
###########################################################
def get_version():
    from QueryReporting.src.version import the_version
    return(get_version())