# -*- coding: utf-8 -*-
__author__ = 'zappyk'

from os     import path, walk, listdir
from shutil import copy2

###############################################################################
def _copy2(file_from, file_to):
    copy2(file_from, file_to)
###############################################################################
def _nameListDir(path_name):
#CZ#files = [ f for f in listdir(path_name) if _os_file._fileExist(path.join(path_name, f)) ]
    names = []
    for (dirpath, dirnames, filenames) in walk(path_name):
        names.extend(filenames)
        break
    return(names)
###############################################################################
def _fileListDir(path_name):
    names = _nameListDir(path_name);
    files = []
    for file_name in names:
        files.append(path_name + file_name)
    return(files)
###############################################################################
def _fileExist(file_name):
    return(path.isfile(file_name))
###############################################################################
def _pathJoin(list_path_file_name):
    return(path.sep.join(list_path_file_name))
###############################################################################
def _pathExpanduser(path_name):
    return(path.expanduser(path_name))
###############################################################################
def _pathAbs(path_name):
    return(path.abspath(path_name))
###############################################################################
def _pathSep():
    return(path.sep)