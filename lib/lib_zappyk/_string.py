# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import re

one_space = ' '
key_crypt = '1!S03r2v19c33s!8.!4P@8yr5017l!6'
utf_codec = 'utf-8'

###############################################################################
def _trim(string):
    return(string.strip())
###############################################################################
def _trimList(string_list):
    list = []
    for string in string_list:
        string = _trim(string)
        list.append(string)
    return(list)
###############################################################################
def _define(then_value, else_value, is_value=None, def_value=None):
    value = def_value
    value = then_value if then_value is not None else else_value
    if is_value is not None:
        if type(is_value) is int:
            if int(value) == is_value:
                value = def_value
        if type(is_value) is str:
            if str(value) == is_value:
                value = def_value
    return(value)
###############################################################################
def _search(regexp, string):
    return(re.search(regexp, string))
###############################################################################
def _findall(regexp, string):
    return(re.findall(regexp, string))
###############################################################################
def _remove(string, remove):
    return(string.rstrip(remove))
###############################################################################
def _replace(string, search, replace):
#CZ#return(string.replace(search, replace))
    return(re.sub(search, replace, string))
###############################################################################
def _joinSpace(string_list):
    return(one_space.join(string_list))
###############################################################################
def _joinChar(string_list, join_char="\n"):
    return(join_char.join(string_list))
###############################################################################
def _removeFirstEmptyLine(string, char="\n"):
    if type(string) is str:
        # deleting first line (if only spaces!) of message :-)
        string_first_line = string.split(char)[0]

        if string_first_line.strip() == '':
            string = char.join(string.split(char)[1:])

    return(string)
###############################################################################
def _stringToList(string, char="\n"):
    if type(string) is str:
        string_list = string.split(char)

        return(string_list)

    return(string)
###############################################################################
def _stringToListOnSpace(string):
    return(_stringToList(string, one_space))
###############################################################################
def _stringToNumber(string, StringInit0=True):
    try:
        if StringInit0:
            import re
            isString = False
            pattern0 = re.compile('^0')
            if pattern0.match(string):
                isString = True
                pattern0 = re.compile('^0\.')
                if pattern0.match(string):
                    isString = False
                pattern0 = re.compile('^0,')
                if pattern0.match(string):
                    isString = False
                pattern0 = re.compile('^0$')
                if pattern0.match(string):
                    isString = False
            if isString:
                return(string)

        return(float(string))
    except ValueError:
        return(string)
###############################################################################
def _crypting(data, key=key_crypt, codec=utf_codec, encode=False):
    import binascii
    from itertools import cycle
    #--------------------------------------------------------------------------
    bin_key = key.encode(codec)
    bin_data = data.encode(codec)

    if not encode: bin_data = binascii.unhexlify(bin_data)

    bin_xored = bytes([x ^ y for x, y in zip(bin_data, cycle(bin_key))])
    #--------------------------------------------------------------------------
    if encode:
        return(binascii.hexlify(bin_xored).decode(codec))
    else:
        return(bin_xored.decode(codec))
