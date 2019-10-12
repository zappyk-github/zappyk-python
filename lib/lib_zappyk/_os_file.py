# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os

from os     import path, walk, listdir
from shutil import copy2, rmtree, make_archive, move

###############################################################################
def _copy2(file_from, file_to):
    copy2(file_from, file_to)
###############################################################################
def _basepath(path_file):
    return(path.dirname(path_file))
###############################################################################
def _basename(path_file):
    return(path.basename(path_file))
###############################################################################
def _basenameNotExt(path_file):
    return(path.splitext(path.basename(path_file))[0])
###############################################################################
#CZ#def _basenameGetExt(path_file):
#CZ#    return(path.splitext(path.basename(path_file))[1])
###############################################################################
def _basenameGetExt(path_file):
    return(path.splitext(path_file)[1])
###############################################################################
def _basenameFullPathNotExt(path_file):
    return(path.splitext(path_file)[0])
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
def _fileMove(file_name_from, file_name_to):
#CZ#return(os.rename(file_name_from, file_name_to))
    return(move(file_name_from, file_name_to))
###############################################################################
def _fileRemove(file_name):
    return(os.remove(file_name))
###############################################################################
def _pathRemove(path_name):
#CZ#return(rmtree(path_name, ignore_errors=True))
    return(rmtree(path_name))
###############################################################################
def _pathExist(path_name):
    return(path.isdir(path_name))
###############################################################################
def _pathJoin(list_path_file_name):
    return(path.sep.join(list_path_file_name))
###############################################################################
def _pathExpanduser(path_name):
    return(path.expanduser(path_name))
###############################################################################
def _pathCurrent():
    return(os.getcwd())
###############################################################################
def _pathAbs(path_name):
    return(path.abspath(path_name))
###############################################################################
def _makeArchive(file_name, file_type='zip', path_name=None):
    return(make_archive(file_name, file_type, path_name))
###############################################################################
def _makeDir(path_name):
    if not os.path.exists(path_name):
        return(os.makedirs(path_name))
    return(True)
###############################################################################
def _pathSep():
    return(path.sep)
