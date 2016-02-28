# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import argparse, configparser

from lib_zappyk._log     import _log
from lib_zappyk._os_file import _pathAbs, _pathJoin, _fileExist, _pathSep, _pathExpanduser

from QueryReporting               import *
from QueryReporting.src.constants import *

_project_     = get_project()
_description_ = get_description()

name_conf = '%s-config.ini' % _project_
path_conf = _pathAbs(_pathJoin(['.']))
file_conf = _pathAbs(_pathJoin([path_conf, name_conf]))

name_logs = '%s-logger.ini' % _project_
path_logs = _pathAbs(_pathJoin(['.']))
file_logs = _pathAbs(_pathJoin([path_logs, name_logs]))

default_query   = DEF_SQLQUERY
default_stdout  = CHAR_STD_INOUT
default_typeout = TYPE_OUT_csv
default_typeout = None
list_typeout    = [TYPE_OUT_csv,TYPE_OUT_xls]
list_drivers    = TYPE_DB_LIST

###############################################################################
class logger_conf(object):
    logs = None
    ###########################################################################
    def __init__(self, name=None):
        if not _fileExist(file_logs):
            print("File logger %s not found!" % (file_logs))

        self.logs = _log(name, file_logs)

###############################################################################
class parser_args(object):
    args = None
    ###########################################################################
    def __init__(self):
        parser = argparse.ArgumentParser(description=_description_)
    #CZ#pgroup = parser.add_mutually_exclusive_group()

    #CZ#pgroup.add_argument('-p'     , '--power'             , help='display a power of a given number' , type=int, choices=[1,2,3,4,5])
    #CZ#pgroup.add_argument('-s'     , '--square'            , help='display a square of a given number', type=int)
        parser.add_argument('-d'     , '--debug'             , help='increase output debug'             , action='count'                , default=0)
        parser.add_argument('-v'     , '--verbose'           , help='output verbosity'                  , action='store_true')
        parser.add_argument('-rg'    , '--run_gui'           , help='run GUI (Graphical User Interface)', action='store_true')
        parser.add_argument('-rc'    , '--run_cmd'           , help='run Command Console'               , action='store_true')
        parser.add_argument('-rq'    , '--run_query'         , help='run query name'                    , type=str                      , default=default_query  ,required=True)
        parser.add_argument('-fo'    , '--file_output'       , help='file write output'                 , type=str                      , default=default_stdout)
        parser.add_argument('-to'    , '--type_output'       , help='file type  output'                 , type=str, choices=list_typeout, default=default_typeout)
        parser.add_argument('-dbdr'  , '--db__driver_'       , help='DB driver'                         , type=str, choices=list_drivers, default=None)
        parser.add_argument('-dbsn'  , '--db__server_'       , help='DB server'                         , type=str                      , default=None)
        parser.add_argument('-dbsp'  , '--db__onport_'       , help='DB server port'                    , type=int                      , default=None)
        parser.add_argument('-dbdb'  , '--db_database'       , help='DB database'                       , type=str                      , default=None)
        parser.add_argument('-dbun'  , '--db_username'       , help='DB username'                       , type=str                      , default=None)
        parser.add_argument('-dbpw'  , '--db_password'       , help='DB password'                       , type=str                      , default=None)
        parser.add_argument('-dbao'  , '--db_add_opts'       , help='DB add options'                    , type=str                      , default=None)
        parser.add_argument('-dbnh'  , '--db_noheader'       , help='DB result not print header'        , action='store_true')
        parser.add_argument('-cdl'   , '--csv_delimiter'     , help='CSV file delimiter char fields'    , type=str                      , default=None)
        parser.add_argument('-cqc'   , '--csv_quotechar'     , help='CSV file quote char fields'        , type=str                      , default=None)
        parser.add_argument('-clt'   , '--csv_lineterminator', help='CSV file line terminator'          , type=str                      , default=None)
    #CZ#parser.add_argument('name'   , help='Name')
    #CZ#parser.add_argument('surname', help='Surnamename')

        args = parser.parse_args()

        self.args = args

###############################################################################
class parser_conf(object):
    conf = None
    ###########################################################################
    def __init__(self):
    #??#conf = configparser.ConfigParser(allow_no_value=True)
        conf = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

        if not _fileExist(file_conf):
            print("File configuration %s not found!" % (file_conf))
            conf = None
        else:
            conf.read(file_conf)
            conf = self.parser_conf_init(conf, 'Os', 'path_join', _pathSep())
            conf = self.parser_conf_init(conf, 'Os', 'path_home', _pathExpanduser('~'))

        self.conf = conf

    ###############################################################################
    def parser_conf_init(self, parser, section, option, value_new):
        value_old = parser.get(section, option, fallback=None)
        if value_old is None:
            parser.set(section, option, value_new)
        return(parser)