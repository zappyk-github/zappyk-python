# -*- coding: utf-8 -*-
__author__ = 'zappyk'

LINE_LENGTH = 80
LINE_LENGTH = 120

TIME_BOX_BRECK = int(LINE_LENGTH / 20)
LINE_BOX_BRECK = '........%<..........' * TIME_BOX_BRECK
LINE_BOX_BRECK = LINE_BOX_BRECK.ljust(LINE_LENGTH, '.')
LINE_SEPARATOR = '#' * LINE_LENGTH