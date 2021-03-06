#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'
########################################################################################################################
import os, sys, platform
#=======================================================================================================================
print(' | platform          : %s' % sys.platform)
print(' | platform machine  : %s' % platform.machine())
print(' | platform processor: %s' % platform.processor())
########################################################################################################################
runas_prog=r"C:\Windows\notepad.exe"
runas_prog=r"C:\Windows\write.exe"
runas_prog=sys.argv[1] if len(sys.argv)>1 else None
#=======================================================================================================================
runas_path=sys.argv[2] if len(sys.argv)>2 else None
#=======================================================================================================================
runas_user=r"PAYROLL\Administrator"
runas_pswd=r"!P@yr01l!"
#=======================================================================================================================
runas_file=r"%s.vbs" % os.path.basename(__file__)
runas_cmmd=r"""
' Load Arguments:
Set args = WScript.Arguments
args0 = args.Item(0)
'WScript.Echo args0

' Load CreateObject:
Set WshShell = WScript.CreateObject("WScript.Shell")

' Open notepad:
'WshShell.Run "notepad.exe", 9

' Give time to load:
WScript.Sleep 1000

' Type in string arguments:
WshShell.SendKeys args0
WshShell.SendKeys "{ENTER}"

' Add the key-function:
'WshShell.SendKeys "{F5}"
"""
#=======================================================================================================================
if runas_prog is None:
    print("Specifica il programma da lanciare come utente \"%s\"..." % runas_user)
    sys.exit(1)
#=======================================================================================================================
if runas_path is not None:
    from shutil import copy2
    runas_prog
    runas_name = os.path.basename(runas_prog)
    runas_copy = os.path.join(runas_path, runas_name)
    print("...copy file \"%s\" on directory \"%s\"..." % (runas_name, runas_path))
    try:
        copy2(runas_prog, runas_copy)
#CZ#except:
    except Exception as e:
        print("ERROR: %s" % str(e))
        sys.exit(1)
    runas_prog = runas_copy
#=======================================================================================================================
print("runas... [%s] process [%s]" % (runas_user, runas_prog))
########################################################################################################################
def _os_system_wbscr(file, cmmd, pswd):
    fo = open(file, "w")
    fo.write(cmmd)
    fo.close()
    os.system("%s \"%s\"" % (file, pswd))
########################################################################################################################
def _os_system_runas(user, prog):
    os.system("runas /noprofile /user:%s \"%s\"" % (user, prog))
########################################################################################################################
def _os_remove_wbscr(file):
    os.remove(file)
########################################################################################################################
_os_system_wbscr(runas_file, runas_cmmd, runas_pswd)
_os_system_runas(runas_user, runas_prog)
_os_remove_wbscr(runas_file)
########################################################################################################################
print("...done!")
sys.exit()