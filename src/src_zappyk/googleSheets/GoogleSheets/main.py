#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys

from GoogleSheets.src import load_run
from GoogleSheets.cfg import load_cfg

#args= load_cfg.parser_args()
conf = load_cfg.parser_conf()
logs = load_cfg.logger_conf()

if conf is None:
    logs.error("Errore bloccante: file di configurazione '%s' mancante!" % load_cfg.file_conf)

if __name__ == '__main__':
    load_run.main()

sys.exit(0)