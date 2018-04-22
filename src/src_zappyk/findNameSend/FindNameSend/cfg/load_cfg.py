# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import argparse, configparser

from lib_zappyk._log     import _log
from lib_zappyk._os_file import _pathAbs, _pathJoin, _fileExist, _pathSep, _pathExpanduser

from FindNameSend import *

_project_     = get_project()
_description_ = get_description()

name_conf = '%s-config.ini' % _project_
path_conf = _pathAbs(_pathJoin(['.']))
file_conf = _pathAbs(_pathJoin([path_conf, name_conf]))

name_logs = '%s-logger.ini' % _project_
path_logs = _pathAbs(_pathJoin(['.']))
file_logs = _pathAbs(_pathJoin([path_logs, name_logs]))

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

    #CZ#pgroup.add_argument('-p'  , '--power'         , help='display a power of a given number' , type=int, choices=[1,2,3,4,5])
    #CZ#pgroup.add_argument('-s'  , '--square'        , help='display a square of a given number', type=int)
        parser.add_argument('-d'  , '--debug'         , help='increase output debug'             , action='count', default=0)
        parser.add_argument('-v'  , '--verbose'       , help='output verbosity'                  , action='store_true')
        parser.add_argument('-nse', '--not_send_email', help='not send any notify email'         , action='store_true')
    #CZ#parser.add_argument('name'                    , help='Name')
    #CZ#parser.add_argument('surname'                 , help='Surname')

        args = parser.parse_args()

        self.args = args

###############################################################################
class parser_conf(object):
    conf = None
    ###########################################################################
    def __init__(self):
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
