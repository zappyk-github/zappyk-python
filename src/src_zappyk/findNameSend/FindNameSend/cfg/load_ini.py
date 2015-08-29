# -*- coding: utf-8 -*-
import os, sys
###############################################################################
_Os_path_join = os.path.sep
_Os_path_home = os.path.expanduser('~')
#==============================================================================
tag_list_base = ['dfs', 'zpinfob', '3.2.0']
tag_list_last = ['schedulazione', 'log']
tag_list__PJ_ = tag_list_base + ['PJHRETL'] + tag_list_last
tag_list__PW_ = tag_list_base + ['PWHRETL'] + tag_list_last
###############################################################################
end_grep_regx = 'ETL FINITO REGOLARMENTE'
end_grep_ifno = '!!! ATTENZIONE, ETL NON REGOLARMENTE FINITO, STRINGA "' + end_grep_regx + '" NON TROVATA !!!'
end_line_back = 20
###############################################################################
tag_name_exte = '*.log'
tag_name_regx = '(.log|.LOG)$'
tag_grep_regx = 'ERROR |failed|false'
tag_line_regx = 'ERROR '
tag_line_init = -5
tag_line_done = 15
tag_find_last = True
###############################################################################
tag_path_base = _Os_path_join.join(tag_list_base)
tag_path_last = _Os_path_join.join(tag_list_last)
###############################################################################
tag_path_find = []
tag_path_find.append(_Os_path_join.join(tag_list__PJ_))
tag_path_find.append(_Os_path_join.join(tag_list__PW_))
###############################################################################
tag_path_desc = []
tag_path_desc.append('PJ (PagheProject)')
tag_path_desc.append('PW (PagheWeb)')
###############################################################################
email_notify_ = True
email__smtp__ =  'smtp.gmail.com:587'
email__from__ =  'pes0zap@payroll.it'
email___to___ = ['pes0zap@payroll.it']
email___cc___ = []
email___ccn__ = []
email_attachs = []
emailfontsize = '2' # (1|2|3|0=None)
email_subject = "ZPINFOB: Notifica ricerca Errori elaborazione ETL: %s"
email_message = """
========================================
   Messaggio automatico da FindNameSend
   Non rispondere a questo indirizzo!
========================================

Qui di seguito, in evidenza, l'elenco degli errori trovati dopo l'elaborazione ETL.
In allegato il file log completo (%s).

[ %s ]
|______________________________________________________________________________________________________________________

%s
_______________________________________________________________________________________________________________________

--

( Information Technology )
P&S Srl - Payroll Services
"""
###############################################################################
emailAuthUser = 'sysop@payroll.it'
emailAuthPswd = 's3rv1c3s'
###############################################################################
