# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os, argparse, configparser

from lib_zappyk._log     import _log
from lib_zappyk._os_file import _os_file

from SwitchOnOff.src.constants import *
from SwitchOnOff               import *

_project_     = get_project()
_description_ = get_description()

name_conf = '%s-config.ini' % _project_
path_conf = os.path.abspath(os.path.join('.'))
file_conf = os.path.abspath(os.path.join(path_conf, name_conf))

name_logs = '%s-logger.ini' % _project_
path_logs = os.path.abspath(os.path.join('.'))
file_logs = os.path.abspath(os.path.join(path_logs, name_logs))

chc_query = [DB_QUERY_CANCEL, DB_QUERY_CREATE, DB_QUERY__LIST_, DB_QUERY_DELETE, DB_QUERY_SELECT, DB_QUERY_UPDATE, DB_QUERY_INSERT]

###############################################################################
class logger_conf(object):
    logs = None
    ###########################################################################
    def __init__(self, name=None):
        if not _os_file._fileExist(file_logs):
            print("File logger %s not found!" % (file_logs))

        self.logs = _log(name, file_logs)

###############################################################################
class parser_args(object):
    args = None
    ###########################################################################
    def __init__(self):
        parser = argparse.ArgumentParser(description=_description_)
    #CZ#group0 = parser.add_mutually_exclusive_group()
        group1 = parser.add_argument_group()
        group2 = parser.add_argument_group()

    #CZ#group0.add_argument('-p'  , '--power'     , help='display a power of a given number' , type=int, choices=[1,2,3,4,5])
    #CZ#group0.add_argument('-s'  , '--square'    , help='display a square of a given number', type=int)
        parser.add_argument('-d'  , '--debug'     , help='increase output debug'             , action='count', default=0)
        parser.add_argument('-v'  , '--verbose'   , help='output verbosity'                  , action='store_true', default=False)
        parser.add_argument('query'               , help='DB Query command'                  , choices=chc_query, default=DB_QUERY__LIST_)
        group1.add_argument('-fn' , '--field-name', help='DB field Name')
        group1.add_argument('-fd' , '--field-desc', help='DB field Desc')
        group1.add_argument('-ff' , '--field-flag', help='DB field Flag')
        group2.add_argument('-on' , '--is-on'     , help='Question flag is On'               , action='store_true', default=False)
        group2.add_argument('-off', '--is-off'    , help='Question flag is Off'              , action='store_true', default=False)
    #CZ#parser.add_argument('name'               , help='Name')
    #CZ#parser.add_argument('surname'            , help='Surnamename')

        args = parser.parse_args()

        logs = logger_conf().logs

        if args.query == DB_QUERY_CANCEL:
            pass
        if args.query == DB_QUERY_CREATE:
            pass
        if args.query == DB_QUERY__LIST_:
            pass
        if args.query == DB_QUERY_DELETE:
            if args.field_name is None:
                parser.print_help()
        if args.query == DB_QUERY_SELECT:
            if args.field_name is None:
                parser.print_help()
                logs.warning("_______________________________________")
                logs.warning("Specifica l'opzione [-fn | --fiel-name]")
                logs.error("  se utilizzi la query [%s] :-|" % DB_QUERY_SELECT)
        if args.query == DB_QUERY_UPDATE:
            if args.field_name is None or\
               args.field_flag is None:
                parser.print_help()
                logs.warning("_________________________________________")
                logs.warning("Specifica l'opzione [-fn | --fiel-name] e")
                logs.warning("          l'opzione [-ff | --fiel-flag]")
                logs.error("  se utilizzi la query [%s] :-|" % DB_QUERY_UPDATE)
        if args.query == DB_QUERY_INSERT:
            if args.field_name is None or\
               args.field_desc is None or\
               args.field_flag is None:
                parser.print_help()
                logs.warning("_________________________________________")
                logs.warning("Specifica l'opzione -fn [ --fiel-name ] e")
                logs.warning("          l'opzione -fd [ --fiel-desc ] e")
                logs.warning("          l'opzione -ff [ --fiel-flag ]")
                logs.error("  se utilizzi la query [%s] :-|" % DB_QUERY_INSERT)

        self.args = args

###############################################################################
class parser_conf(object):
    conf = None
    ###########################################################################
    def __init__(self):
        conf = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

        if not _os_file._fileExist(file_conf):
            print("File configuration %s not found!" % (file_conf))
            conf = None
        else:
            conf.read(file_conf)
            conf = self.parser_conf_init(conf, 'Os', 'path_join', os.path.sep)

        self.conf = conf

    ###############################################################################
    def parser_conf_init(self, parser, section, option, value_new):
        value_old = parser.get(section, option, fallback=None)
        if value_old is None:
            parser.set(section, option, value_new)
        return(parser)