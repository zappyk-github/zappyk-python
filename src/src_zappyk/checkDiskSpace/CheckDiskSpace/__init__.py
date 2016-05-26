# -*- coding: utf-8 -*-
__author__ = 'pes0zap'

PROJECT     = 'CheckDiskSpace'
DESCRIPTION = """
Return disk usage statistics about the given path as a (total, used, free)
namedtuple. Values are expressed in bytes or human unit measure.
"""
VERSION     = (0, 1, 0, 'rc'  , 1)
VERSION     = '0.1'
VERSION     = '0.2'
VERSION     = '0.2-1'
VERSION     = '0.2-2'

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