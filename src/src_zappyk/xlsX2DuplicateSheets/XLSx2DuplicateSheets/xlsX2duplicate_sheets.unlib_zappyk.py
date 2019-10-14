#!/usr/bin/env python-payroll
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys, argparse #, configparser
import xlrd #, xlwt
import openpyxl

from xlutils import copy

#CZ#from lib_zappyk._os_file import _makeDir, _pathExist, _pathRemove, _basename, _basepath, _pathJoin, _pathCurrent, _pathSep, _copy2, _makeArchive
#CZ#from lib_zappyk._string  import _replace
#CZ#from lib_zappyk._log     import _log
import os
import re
import traceback
import logging
import logging.config
from os     import path
#CZ#from shutil import copy2, rmtree, make_archive
#CZ#try:
#CZ#    from shutil import copy2, rmtree, make_archive
#CZ#except ImportError:
#CZ#    from shutil import copy2, rmtree #, make_archive
#CZ#    from shutil_zappyk.shutil_zappyk import make_archive

_version = '0.1'

_project = 'XLSx2DuplicateSheets'

_description = '''
Duplicate a Spreadsheet ( .xls / .xlsx ) in many workbooks from list
according to the file contain the description of each sheet name.
'''

_epilog = "Version: %s" % _version

_duplicates_ = ['Pippo Matteo', 'Pluto Andrea', 'Paperino Carlo']
_archive_ext = ['zip', 'tar', 'gztar', 'bztar', 'xztar']
_archive_set = _archive_ext[0]
_tag_output_ = '(WorkBookDuplicate)~'

########################################################################################################################

            #        ###  ######          #######     #     ######   ######   #     #  #    #
            #         #   #     #              #     # #    #     #  #     #   #   #   #   #
            #         #   #     #             #     #   #   #     #  #     #    # #    #  #
            #         #   ######            #      #     #  ######   ######      #     ###
            #         #   #     #          #       #######  #        #           #     #  #
            #         #   #     #         #        #     #  #        #           #     #   #
            #######  ###  ######   #####  #######  #     #  #        #           #     #    #

########################################################################################################################
###############################################################################
class _log(object):
    ###########################################################################
    def __init__(self, name=None, file=None):
        if file != None:
            if os.path.isfile(file):
                logging.config.fileConfig(file)

        if name != None:
            self = logging.getLogger(name)
        else:
            self = logging.getLogger(__name__)

    ###########################################################################
    def info(self, string=None, end=None):
        sys.stdout.write(('' if string is None else string) + (os.linesep if end is None else end)) # on python2
    #CZ#print(string, end=end, file=sys.stdout)                                                     # on python3

    ###########################################################################
    def warning(self, string=None, end=None):
        sys.stderr.write(('' if string is None else string) + (os.linesep if end is None else end)) # on python2
    #CZ#print(string, end=end, file=sys.stderr)                                                     # on python3

    ###########################################################################
    def error(self, string=None, end=None, exit_code=1):
        sys.stderr.write(('' if string is None else string) + (os.linesep if end is None else end)) # on python2
    #CZ#print(string, end=end, file=sys.stderr)                                                     # on python3
        sys.exit(exit_code)

    ###########################################################################
    def traceback(self, exc_traceback=None, limit=1, file=sys.stderr):
        traceback.print_tb(exc_traceback, limit=limit, file=file)
###########################################################################
def _replace(string, search, replace):
#CZ#return(string.replace(search, replace))
    return (re.sub(search, replace, string))
###############################################################################
def _makeDir(path_name):
    if not os.path.exists(path_name):
        return(os.makedirs(path_name))
    return(True)
###############################################################################
def _pathSep():
    return(path.sep)
###############################################################################
def _pathRemove(path_name):
#CZ#return(rmtree(path_name, ignore_errors=True))
    return(rmtree(path_name))
###############################################################################
def _pathExist(path_name):
    return(path.isdir(path_name))
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
def _makeArchive(file_name, file_type='zip', path_name=None):
    return(make_archive(file_name, file_type, path_name))
###############################################################################
def _pathJoin(list_path_file_name):
    return(path.sep.join(list_path_file_name))
########################################################################################################################
########################################################################################################################

logs = _log()

###############################################################################
def _getargs():
#CZ#parser = argparse.ArgumentParser(description=_description, epilog=_epilog, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=120)
    formatter = lambda prog: argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=50, width=120)
#CZ#formatter = lambda prog: argparse.RawDescriptionHelpFormatter(prog, max_help_position=50, width=120)
    parser = argparse.ArgumentParser(description=_description, epilog=_epilog, formatter_class=formatter) #, argument_default=not argparse.SUPPRESS)

#CZ#pgroup.add_argument('-p' , '--power'          , help='display a power of a given number'   , type=int           , choices=[1,2,3,4,5])
#CZ#pgroup.add_argument('-s' , '--square'         , help='display a square of a given number'  , type=int)
    parser.add_argument('-d' , '--debug'          , help='increase output debug'               , action='count'     , default=0)
    parser.add_argument('-v' , '--verbose'        , help='output verbosity'                    , action='store_true')
    parser.add_argument('-V' , '--version'        , help='print version number'                , action='version'   , version='%(prog)s '+_version)
    parser.add_argument('-fi', '--file_input'     , help='file spreadsheet (only .xls/.xlsx)'  , type=str           , required=True)
    parser.add_argument('-bs', '--base_sheet'     , help='duplicate sheet by name'             , type=str           , required=True)
    parser.add_argument('-to', '--tag_output'     , help='name new file output'                , type=str           , default=_tag_output_)
#CZ#parser.add_argument('-as', '--archive_set'    , help='select archive format'               , type=str           , default=_archive_set, choices=_archive_ext)
#CZ#parser.add_argument('name'                    , help='Name')
#CZ#parser.add_argument('surname'                 , help='Surname')

    args = parser.parse_args()

    return(args)

###############################################################################
class ExceptionFileInputNotParsed(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

###############################################################################
def open_file_input(file_input):
    workbook = None
    xlsx_ext = None

    exception = None

    if workbook is None:
        try:
            workbook = open_file_xlsx(file_input)
            xlsx_ext = True
        except Exception as e:
            exception = e
            pass
        finally:
            if args.debug:
                logs.info('...try open .xlsx format... ', '')
                if workbook is None:
                    logs.info('no! :-(')
                else:
                    logs.info('yes :-)')

    if workbook is None:
        try:
            workbook = open_file_xls_(file_input)
            xlsx_ext = False
        except Exception as e:
            exception = e
            pass
        finally:
            if args.debug:
                logs.info('...try open .xls  format... ', '')
                if workbook is None:
                    logs.info('no! :-(')
                else:
                    logs.info('yes :-)')

    if workbook is None:
        if exception is not None:
            if str(exception) == 'formatting_info=True not yet implemented':
            #CZ#raise ExceptionFileInputNotParsed('File is not .xls/.xlsx format!')
                raise Exception('File is not .xls/.xlsx format!')
            else:
                raise Exception(str(exception))
        else:
            raise Exception('Something is wrong, file not opened!')
    else:
        logs.info('Opened file successfully')

    return(workbook, xlsx_ext)

###############################################################################
def open_file_xlsx(file_input):
    workbook = openpyxl.load_workbook(file_input, data_only=True)
    return(workbook)

###############################################################################
def open_file_xls_(file_input):
#CZ#workbook = xlrd.open_workbook(file_input)
    workbook = xlrd.open_workbook(file_input, formatting_info=True)
    return(workbook)

###############################################################################
def make_name_input(name_input):
    name_input = _replace(name_input, '.xlsx$', '')
    name_input = _replace(name_input, '.xls$' , '')
    return(name_input)

###############################################################################
def make_path_split(path_split):
    if _pathExist(path_split):
        _pathRemove(path_split)
        if _pathExist(path_split):
            logs.error('Cannot remove directory [%s]' % path_split)
        else:
            _makeDir(path_split)
    else:
        _makeDir(path_split)
    return(path_split)

###############################################################################
if __name__ == '__main__':
    args = _getargs()

    base_sheet = args.base_sheet
    file_input = args.file_input
#CZ#archiveset = args.archive_set
    tag_output = args.tag_output
    nameoutput = (tag_output, _basename(file_input))
    pathoutput = (_basepath(file_input), ''.join(nameoutput))
    fileoutput = _pathJoin(pathoutput)

    name_input = _basename(file_input)

    try:
        logs.info('[%s]' % _pathCurrent())
        logs.info('Duplicate Worksheet "%s" to list sheetname %s' % (base_sheet, _duplicates_))
        logs.info('Open file "%s" for duplicate:' % file_input)
        (workbook
        ,xlsx_ext) = open_file_input(file_input)

#CZ#except ExceptionFileInputNotParsed as e:
#CZ#    logs.error(str(e))
    except Exception as e:
        logs.error(str(e))

    try:
        target = workbook[base_sheet]
        logs.info('Worksheet "%s" found :-)' % base_sheet)
    except Exception as e:
        logs.info('Worksheet not found! :-(')
        logs.error(str(e))
        sys.exit(1)

    for i in range(0, len(_duplicates_)):
        logs.info('· Duplicate sheetbase #%s for "%s"' % ((i + 1), _duplicates_[i]))
        workbook.copy_worksheet(target)

    i = 0
    for sheet in workbook:
        j = '' if i == 0 else str(i)
        base_sheet_copy = ('%s Copy%s' % (base_sheet, j))
        logs.info('· Title sheet %-20s ' % ('"%s"' % (sheet.title)), end='')
        if sheet.title == base_sheet:
            logs.info('...skip title sheetbase...')
        elif sheet.title == base_sheet_copy:
            sheet.title = _duplicates_[i]
            i = i + 1
            logs.info('replace title #%s for "%s"' % (i, sheet.title))
        else:
            logs.info('...skip title sheet...')

    logs.info('Save file: "%s"' % (fileoutput))
    workbook.save(fileoutput)

    '''
    try:
        logs.info()
        logs.info('Create %s archive %s' % (archiveset, file_press + '.' + archiveset))
        _makeArchive(file_press, archiveset, path_split)
        logs.info('Create %s archive successfully' % archiveset)

        if not args.debug:
            _pathRemove(path_split)
    except Exception as e:
        logs.info('Create %s archive failed  :-( ' % archiveset)
        logs.error(str(e))
    '''

    sys.exit(0)
