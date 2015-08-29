# -*- coding: utf-8 -*-
__author__ = 'pes0zap'

import re

###########################################################################
def _search(regexp, string):
    return(re.search(regexp, string))
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