# -*- coding: utf-8 -*-
__author__ = 'pes0zap'

import re

one_space = ' '

###########################################################################
def _trim(string):
    return(string.strip())
###########################################################################
def _trimList(string_list):
    list = []
    for string in string_list:
        string = _trim(string)
        list.append(string)
    return(list)
###########################################################################
def _search(regexp, string):
    return(re.search(regexp, string))
###########################################################################
def _findall(regexp, string):
    return(re.findall(regexp, string))
###########################################################################
def _remove(string, remove):
    return(string.rstrip(remove))
###########################################################################
def _replace(string, search, replace):
    return(re.replace(search, replace, string))
###########################################################################
def _joinSpace(string_list):
    return(one_space.join(string_list))
###########################################################################
def _removeFirstEmptyLine(string, char="\n"):
    if type(string) is str:
        # deleting first line (if only spaces!) of message :-)
        string_first_line = string.split(char)[0]

        if string_first_line.strip() == '':
            string = char.join(string.split(char)[1:])

    return(string)
###########################################################################
def _stringToList(string, char="\n"):
    if type(string) is str:
        string_list = string.split(char)

        return(string_list)

    return(string)
###########################################################################
def _stringToListOnSpace(string):
    return(_stringToList(string, one_space))
