# -*- coding: utf-8 -*-
__author__ = 'zappyk'

from os     import path, listdir, walk
from shutil import copy2

###############################################################################
class _os_file:
    ###########################################################################
    def _fileExist(file_name):
        if path.isfile(file_name):
            return(True)
        else:
            return(False)
    ###########################################################################
    def _copy2(file_from, file_to):
        copy2(file_from, file_to)
    ###########################################################################
    def _nameListDir(path_name):
    #CZ#files = [ f for f in listdir(path_name) if _os_file._fileExist(path.join(path_name, f)) ]
        names = []
        for (dirpath, dirnames, filenames) in walk(path_name):
            names.extend(filenames)
            break
        return(names)
    ###########################################################################
    def _fileListDir(path_name):
        names = _os_file._nameListDir(path_name);
        files = []
        for file_name in names:
            files.append(path_name + file_name)
        return(files)
    ###########################################################################
    def _pathJoin(path_name, file_name):
        return(path.sep.join(path_name, file_name))