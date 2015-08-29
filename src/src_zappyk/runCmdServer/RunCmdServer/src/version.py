# -*- coding: utf-8 -*-
__author__ = 'zappyk'

from lib_zappyk._setup import _get_version

def get_version(version=None):
    if version is None:
        from RunCmdServer import VERSION as version
    return(_get_version(version))
