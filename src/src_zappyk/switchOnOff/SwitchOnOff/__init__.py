# -*- coding: utf-8 -*-
__author__ = 'zappyk'

PROJECT     = 'SwitchOnOff'
DESCRIPTION = 'Switch On/Off semaphore'
VERSION     = (0, 0, 1, 'beta', 1)
VERSION     = (0, 1, 0, 'rc'  , 1)

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
#   from SwitchOnOff.src.version import get_version
#   return(get_version(*arg, **kwargs))
###########################################################
def get_version():
    from SwitchOnOff.src.version import get_version
    return(get_version())
