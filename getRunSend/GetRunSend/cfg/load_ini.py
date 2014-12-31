# -*- coding: utf-8 -*-
import os
###############################################################################
_Os_path_join = os.path.sep
_Os_name_prog = """ "C:\Windows\system32\notepad.exe" """
###############################################################################
tag_file_name = "TXDATI.txt"
tag_down_path = "."
tag_down_name = os.path.abspath(os.path.join(tag_down_path, "WgetDownload_" + tag_file_name))
tag_load_path = "."
tag_load_name = os.path.abspath(os.path.join(tag_load_path, "WgetLoadFile_" + tag_file_name))
###############################################################################
url_path_name = "http://apps.payroll.it/pub/"
url_file_name = tag_file_name
url_path_file = url_path_name + "." + url_file_name
#url_proxyhost = {'http': 'http://www.someproxy.com:3128'}
#url_proxyhost = {}
###############################################################################
commands_exec = False
commands_open = """ %s "%s" """ % (_Os_name_prog, tag_load_name)
time_for_loop = 30
###############################################################################
email_notify_ = False
email__smtp__ =  'smtp.gmail.com:587'
email__from__ =  'pes0zap@payroll.it'
email___to___ = ['pes0zap@payroll.it']
email___cc___ = []
email___ccn__ = []
email_attachs = []
emailfontsize = '2' # (1|2|3|0=None)
email_subject = "BestWestern: Notifica caricamento Anagrafico Orologi GONG"
email_message = """
========================================
   Messaggio automatico da GetRunSend
   Non rispondere a questo indirizzo!
========================================

Effettuato caricamento file Anagrafico su Orologi GONG di BestWestern.

_____________________________________
Qui di seguito, l'output del comando:
%s
(exit code %d)

Controllare eventuali anomalie.

________________________________________
Qui di seguito, il tracciato Anagrafico:

%s

--

( Information Technology )
P&S Srl - Payroll Services
"""
###############################################################################
emailAuthUser = 'sysop@payroll.it'
emailAuthPswd = 's3rv1c3s'
###############################################################################