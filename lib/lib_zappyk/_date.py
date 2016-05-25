# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import datetime

###########################################################################
def _dateNow():
    return(datetime.datetime.now())
###########################################################################
def _dateNowFormat(format=None):
    if format is None:
        return(_dateNow())
    else:
        return(_dateNow().strftime(format))
###########################################################################
def _dateNowISOFormat():
    return(_dateNow().isoformat())