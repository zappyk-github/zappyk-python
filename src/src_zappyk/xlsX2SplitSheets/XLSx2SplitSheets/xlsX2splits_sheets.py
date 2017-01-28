#!/usr/bin/env python-payroll
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys, argparse, copy #, configparser
import xlrd #, xlwt
import openpyxl
import shutil

from lib_zappyk._os_file import _makeDir, _pathSep, _pathExist, _pathRemove, _basename, _copy2
from lib_zappyk._string  import _replace
from lib_zappyk._log     import _log

_version = '0.1'

_project = 'XLSx2SplitSheets'

_description = '''
It splits a Spreadsheet ( .xls / .xlsx ) in so many files grouped
according to the first N characters of the name of each sheet name.
'''

_epilog = "Version: %s" % _version

_group_sheet = 6

logs = _log()

###############################################################################
def _getargs():
#CZ#parser = argparse.ArgumentParser(description=_description, epilog=_epilog, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=120)
    formatter = lambda prog: argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=50, width=120)
    formatter = lambda prog: argparse.RawDescriptionHelpFormatter(prog, max_help_position=50, width=120)
    parser = argparse.ArgumentParser(description=_description, epilog=_epilog, formatter_class=formatter) #, argument_default=not argparse.SUPPRESS)

#CZ#pgroup.add_argument('-p' , '--power'       , help='display a power of a given number'    , type=int           , choices=[1,2,3,4,5])
#CZ#pgroup.add_argument('-s' , '--square'      , help='display a square of a given number'   , type=int)
    parser.add_argument('-d' , '--debug'       , help='increase output debug'                , action='count'     , default=0)
    parser.add_argument('-v' , '--verbose'     , help='output verbosity'                     , action='store_true')
    parser.add_argument('-V' , '--version'     , help='print version number'                 , action='version'   , version='%(prog)s '+_version)
    parser.add_argument('-us', '--unit_sheet'  , help='grouped sheet by first char'          , type=int           , default=_group_sheet)
    parser.add_argument('-fi', '--file_input'  , help='file spreadsheet (only .xls/.xlsx)'   , type=str           , required=True)
#CZ#parser.add_argument('name'                 , help='Name')
#CZ#parser.add_argument('surname'              , help='Surnamename')

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
    name_input = _replace(name_input, '.xls$' , '')
    name_input = _replace(name_input, '.xlsx$', '')
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

    unit_sheet = args.unit_sheet
    file_input = args.file_input
    unit_sheet = 3
    file_input = './resources/excel-examples-1.xls'
    #file_input = './resources/excel-wrong.xlsd'
    #args.debug = True

    name_input = _basename(file_input)

    try:
        logs.info('Open file "%s" (splits first %s characters)' % (file_input, unit_sheet))
        (workbook
        ,xlsx_ext) = open_file_input(file_input)

        path_input = make_name_input(file_input)
        path_split = make_path_split(path_input + '.d')
        file_press = path_input
#CZ#except ExceptionFileInputNotParsed as e:
#CZ#    logs.error(str(e))
    except Exception as e:
        logs.error(str(e))

    sheet_names = None
    if xlsx_ext:
        sheet_names = workbook.get_sheet_names()
    else:
        sheet_names = workbook.sheet_names()

    sheet_first = None
    sheet_group = {}
    sheet_puorg = {}
    for sheet_name_ in sheet_names:
        sheet_first = sheet_name_[:unit_sheet]
        sheet_tuple = sheet_group.get(sheet_first, [])
        sheet_tuple.append(sheet_name_)
        sheet_group[sheet_first] = sheet_tuple
        sheet_puorg[sheet_name_] = sheet_first
        logs.info('Sheets[%s] = %s' % (sheet_first, sheet_name_))

    #-------------------------------------------------------------------------------------------------------------------
    if args.debug:
        for sheet_first in sheet_group:
            logs.info('__________')
            logs.info('Group     [%s]' % sheet_first)
            for sheet_name in sheet_group[sheet_first]:
               logs.info('     Sheet[%s]' % sheet_name)
    # ------------------------------------------------------------------------------------------------------------------

    for sheet_first in sheet_group:
        logs.info('__________')
        logs.info('Group     [%s]' % sheet_first)

        name_output = _replace(name_input, '.xls', (' # %s.xls' % sheet_first))
        file_output = path_split + _pathSep() + name_output

        _copy2(file_input, file_output)

        workbook_output = None
        workbook_outxls = None
        if xlsx_ext:
            workbook_output = open_file_xlsx(file_output)
        else:
            workbook_output = open_file_xls_(file_output)
            workbook_outxls = copy.copy(workbook_output)

        for sheet_name_ in sheet_names:
            sheet_keep = sheet_puorg.get(sheet_name_, '')
            if sheet_first == sheet_keep:
                logs.info('  ++ Sheet[%s]' % sheet_name_)
            else:
                logs.info('  -- Sheet[%s]' % sheet_name_)
                if xlsx_ext:
                    workbook_output.remove_sheet(workbook_output.get_sheet_by_name(sheet_name_))
                else:
                    #workbook_outxls = copy.copy(workbook_output)
                    print('...qui...')
                    workbook_outxls._Workbook__worksheets = [ worksheet for worksheet in workbook_outxls._Workbook__worksheets if worksheet.name != sheet_name_ ]

        logs.info('  File Out[%s]' % file_output)
        if xlsx_ext:
            workbook_output.save(file_output)
        else:
            workbook_outxls.save(file_output)

    try:
        logs.info()
        logs.info('Create zip archive %s' % file_press)
        shutil.make_archive(file_press, 'zip', path_split)
        logs.info('Create zip archive successfully')

        if not args.debug:
            _pathRemove(path_split)
    except Exception as e:
        logs.info('Create zip archive failed  :-( ')
        logs.error(str(e))

    sys.exit(0)
