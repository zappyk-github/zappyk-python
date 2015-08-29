# -*- coding: utf-8 -*-
__author__ = 'zappyk'

RUN_SERVER = 'server'
RUN_CLIENT = 'client'

TAG_LOG_CHAR = '#'
TAG_LOG_LENG = 80 - len(TAG_LOG_CHAR)

TAG_COMMAND_EXIT = 'command_exit'
TAG_COMMAND_LOGS = 'command_logs'

TAG_SERPID = '%1s%5s'
TAG_SEPPID = ':'
TAG_FORMAT = "%s %s |%s| %s"
NOW_FORMAT = '%Y%m%d %H:%M.%S'

URI_CHARhp = ':'
URI_CHARrc = '|'
URI_FORMAT = '%s' +URI_CHARhp+ '%s' +URI_CHARrc+ '%s'