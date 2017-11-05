# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os, sys, time, traceback
import logging
import logging.config

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

        self.format = None

    ###########################################################################
    def info(self, string=None, end=None):
        string = self._putFormat(string)
        sys.stdout.write(('' if string is None else string) + (os.linesep if end is None else end)) # on python2
    #CZ#print(string, end=end, file=sys.stdout)                                                     # on python3

    ###########################################################################
    def warning(self, string=None, end=None):
        string = self._putFormat(string)
        sys.stderr.write(('' if string is None else string) + (os.linesep if end is None else end)) # on python2
    #CZ#print(string, end=end, file=sys.stderr)                                                     # on python3

    ###########################################################################
    def error(self, string=None, end=None, exit_code=1):
        string = self._putFormat(string)
        sys.stderr.write(('' if string is None else string) + (os.linesep if end is None else end)) # on python2
    #CZ#print(string, end=end, file=sys.stderr)                                                     # on python3
        sys.exit(exit_code)

    ###########################################################################
    def traceback(self, exc_traceback=None, limit=1, file=sys.stderr):
        traceback.print_tb(exc_traceback, limit=limit, file=file)

    ###########################################################################
    def setFormat(self, format):
        self.format = format
    #--------------------------------------------------------------------------
    def getFormat(self):
        return(self.format)
    #--------------------------------------------------------------------------
    def _putFormat(self, string=None):
        if self.format is not None:
            string = '%s%s' % (self._tagFormat(self.format), '' if string is None else string)
        return(string)
    #--------------------------------------------------------------------------
    def _tagFormat(self, string=None):
        if string is not None:
            string = time.strftime(string)
        return(string)