#!/usr/bin/env python-payroll
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys, argparse #, configparser
import xlrd #, xlwt
import openpyxl

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
if __name__ == '__main__':
    args = _getargs()

    unit_sheet = args.unit_sheet
    file_input = args.file_input
    file_input = '../resources/test.xlsx'
    name_input = _basename(file_input)

    path_split = file_input
    path_split = _replace(path_split, '.xls$' , '.d')
    path_split = _replace(path_split, '.xlsx$', '.d')

    if _pathExist(path_split):
        _pathRemove(path_split)
        if _pathExist(path_split):
            logs.error('Cannot remove directory [%s]' % path_split)
            sys.exit(1)
        else:
            _makeDir(path_split)
    else:
        _makeDir(path_split)

    xlsx_ext = None
    workbook = None

    logs.info('Open file "%s" (splits first %s characters)' % (file_input, unit_sheet))
    try:
        if workbook is None:
            try:
                workbook = openpyxl.load_workbook(file_input, data_only=True)
                xlsx_ext = True
            except FileNotFoundError:
                raise
            except:
                pass
        if workbook is None:
            try:
                workbook = xlrd.open_workbook(file_input, formatting_info=True)
                xlsx_ext = False
            except FileNotFoundError:
                raise
            except:
                pass
        if workbook is None:
            raise ExceptionFileInputNotParsed('File is not .xls/.xlsx format!')
    except FileNotFoundError as e:
        logs.error(str(e))
    except ExceptionFileInputNotParsed as e:
        logs.error(str(e))
    finally:
        if workbook is not None:
            logs.info('Opened file successfully')
        #CZ#sys.exit(0)
        else:
            logs.error('Something is wrong, file not opened!')
            sys.exit(1)

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
#CZ#for sheet_first in sheet_group:
#CZ#    logs.info('__________')
#CZ#    logs.info('Group     [%s]' % sheet_first)
#CZ#    for sheet_name in sheet_group[sheet_first]:
#CZ#        logs.info('     Sheet[%s]' % sheet_name)
    # -------------------------------------------------------------------------------------------------------------------
    for sheet_first in sheet_group:
        logs.info('__________')
        logs.info('Group     [%s]' % sheet_first)

        name_output = _replace(name_input, '.xls', (' # %s.xls' % sheet_first))
        file_output = path_split + _pathSep() + name_output

        _copy2(file_input, file_output)

        workbook_output = None
        if xlsx_ext:
            workbook_output = openpyxl.load_workbook(file_output, data_only=True)
        else:
            workbook_output = xlrd.open_workbook(file_output, formatting_info=True)

        for sheet_name_ in sheet_names:
            sheet_keep = sheet_puorg.get(sheet_name_, '')
            if sheet_first == sheet_keep:
                logs.info('  ++ Sheet[%s]' % sheet_name_)
            else:
                logs.info('  -- Sheet[%s]' % sheet_name_)
                if xlsx_ext:
                    workbook_output.remove_sheet(workbook_output.get_sheet_by_name(sheet_name_))
                else:
                    print('...devel remove sheet XLS...')

        logs.info('  File Out[%s]' % file_output)
        workbook_output.save(file_output)

    print('...devel create zip...')

    sys.exit(0)
