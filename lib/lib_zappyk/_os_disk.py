# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os, collections

###############################################################################
def _disk_usage(path_name):
    from lib_zappyk._os import _os_linux, _os_windows

    _disk_usage_ntuple = collections.namedtuple('usage', 'total used free')

    # LINUX :
    #==========================================================================
    if _os_linux:
        _ = os.statvfs(path_name)
        free = _.f_bavail * _.f_frsize
        total = _.f_blocks * _.f_frsize
        used = (_.f_blocks - _.f_bfree) * _.f_frsize
        return(_disk_usage_ntuple(total, used, free))

    # WINDOWS :
    #==========================================================================
    elif _os_windows:
        import ctypes
        import sys

        (used, total, free) = (ctypes.c_ulonglong(), ctypes.c_ulonglong(), ctypes.c_ulonglong())
    #CZ#if sys.version_info >= (3,) or isinstance(path_name, unicode):
        if sys.version_info >= (3,):
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW
        else:
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA
        ret = fun(path_name, ctypes.byref(used), ctypes.byref(total), ctypes.byref(free))
        if ret == 0:
            raise(ctypes.WinError())
        used_value = total.value - free.value
        return(_disk_usage_ntuple(total.value, used_value, free.value))

    raise(NotImplementedError('platform not supported'))