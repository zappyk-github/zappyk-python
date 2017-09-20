#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'
########################################################################################################################
import os, sys, platform
#=======================================================================================================================
print(' · platform          : %s' % sys.platform)
print(' · platform machine  : %s' % platform.machine())
print(' · platform processor: %s' % platform.processor())
########################################################################################################################
runas_user=r"PAYROLL\Administrator"
runas_pswd=r"!P@yr01l!"
#=======================================================================================================================
runas_cmmd=r"cmd"
runas_cmmd=r"%s\system32\cmd.exe" % os.environ['windir']
#=======================================================================================================================
runas_prog=r"notepad.exe"
runas_prog=r"C:\Windows\notepad.exe"
#runas_prog=runas_cmmd
#=======================================================================================================================
print('runas... ['+runas_user+'] process ['+runas_prog+']')
########################################################################################################################
def _subprocess_call():
    import subprocess
    process = subprocess.call(['runas', '/noprofile', '/user:' + runas_user, runas_prog])
   #process = subprocess.call(['runas', '/noprofile', '/user:'+runas_user, runas_prog], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   #process = subprocess.call(['runas', '/noprofile', '/user:'+runas_user, runas_prog], stdin=subprocess.PIPE, shell=True)
    process.wait()
    process.stdin.write(runas_pswd + "\r\n")
    process.stdin.close()
   #subprocess.call(['cmd'], shell=True)
########################################################################################################################
def _pywinauto_application():
    from pywinauto import application
    myapp = application.Application()
    mycmd = application.Application.Start(myapp, cmd_line=runas_prog)
   #mycmd.top_window_().TypeKeys(runas_user+'{ENTER}')
   #mycmd.top_window_().TypeKeys(runas_pswd+'{ENTER}')
    mycmd.top_window_().TypeKeys("Ciao{TAB}pirla{ENTER}")
########################################################################################################################
def _os_system():
   #os.system("runas /noprofile /user:%s %s" % (runas_user, runas_prog))
    os.system("%s" % runas_prog)
########################################################################################################################
#_subprocess_call()
#_pywinauto_application()
_os_system()
########################################################################################################################
print('...done!')
sys.exit()
