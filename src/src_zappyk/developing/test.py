#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

########################################################################################################################
import sys, platform

print(sys.platform)
print(platform.machine())
print(platform.processor())

########################################################################################################################
import subprocess

runas_user='PAYROLL\Administrator'
runas_pswd='!P@yr01l!'
runas_prog='cmd'
runas_prog='notepad.exe'

print('runas ['+runas_user+'] process ['+runas_prog+']')

#process = subprocess.call(['runas', '/noprofile', '/user:'+runas_user, runas_prog])
#process = subprocess.call(['runas', '/noprofile', '/user:'+runas_user, runas_prog], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#process = subprocess.call(['runas', '/noprofile', '/user:'+runas_user, runas_prog], stdin=subprocess.PIPE, shell=True)
#process.wait()
#process.stdin.write(runas_pswd+"\r\n")
#process.stdin.close()

#subprocess.call(['cmd'], shell=True)

print('done.')
#=======================================================================================================================
from pywinauto import application
#myapp = application.Application()
#app = application.Application.Start(myapp, cmd_line=r"notepad.exe")
#app.top_window_().TypeKeys("PAYROLL\Administrator{ENTER}")
#app.top_window_().TypeKeys("!P@yr01l!{ENTER}")
#app.top_window_().TypeKeys("Ciao{TAB}pirla{ENTER}")
########################################################################################################################