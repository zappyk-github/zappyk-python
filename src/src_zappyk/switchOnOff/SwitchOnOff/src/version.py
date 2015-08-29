# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os, subprocess, datetime

from lib_zappyk import _setup

def get_version(version=None):
    if version is None:
        from switchOnOff.SwitchOnOff import VERSION as version
    return(_setup._get_version(version))
