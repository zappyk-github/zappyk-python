#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'pes0zap'

import os, sys
import argparse #, configparser

from lib_zappyk._os      import _os_host_type, _os_host_name
from lib_zappyk._os_disk import _os_disk
from lib_zappyk._email   import _email
from lib_zappyk._manip   import _bytes_human_manip

_version = '0.2'

_project = 'CheckDiskSpace'

_description = '''
Return disk usage statistics about the given path as a (total, used, free)
namedtuple. Values are expressed in bytes or human unit measure.

Replace variables:
  *  %path_base% with base path
  *  %host_type% with type host
  *  %host_name% with name host
'''

_epilog = "Version: %s" % _version

_mail_message_sep = '''
_______________________________________________________________________________
'''

_mail_host    = 'smtp.payroll.it'
_mail_from    = 'it@payroll.it'
_mail_subject = 'Alert space on $host_name$ ($host_type$) mount $path_base$'
_mail_message = """
Check disk space on path base: %s

[ total= %s | used= %s | free= %s ]
"""

_message_alert = 'Attention, free space below limit! [= %s ] :-('
_message_allok = 'All right, free space over limit [= %s ] :-)'

###############################################################################
def _sendmail_prepare(args, message_print, message_alert):

    message_email = [message_print, message_alert]
    if args.mail_message is not None:
        message_email.insert(0, _mail_message_sep)
        message_email.insert(0, args.mail_message)
    args.mail_message = "\n".join(message_email)

    args.mail_subject = _replaces(args.mail_subject, _path_base=path_base)
    args.mail_message = _replaces(args.mail_message, _path_base=path_base)

    if args.mail_to is None:
        args.mail_to = '';

    if args.mail_cc is None:
        args.mail_cc = '';

    return(args)

###############################################################################
def _sendmail(args):
    email_ongmail = args.gmail
    email__send__ = args.send_mail
    email__smtp__ = args.mail_host
    emailStartTLS = False
    emailAuthUser = None
    emailAuthPswd = None
    email__from__ =  args.mail_from
    email___to___ =  args.mail_to
    email___cc___ = [args.mail_cc]
    email___ccn__ = []
    email_attachs = []
    emailfontsize = None
    email__subj__ = args.mail_subject
    email__body__ = args.mail_message

    if email__send__:
        send_email = _email()
    #CZ#send_email._setMailSmtp        (email__smtp__)
    #CZ#send_email._setMailAuthUser    (emailAuthUser)
    #CZ#send_email._setMailAuthPswd    (emailAuthPswd)
    #CZ#send_email._setMailFrom        (email__from__)
        send_email._setMailTo          (email___to___)
        send_email._setMailCc          (email___cc___)
    #CZ#send_email._setMailCcn         (email___ccn__)
    #CZ#send_email._setMailAttachs     (email_attachs)
    #CZ#send_email._setMailHtmlFontSize(emailfontsize)
        send_email._setMailSubject     (email__subj__)
        send_email._setMailMessage     (email__body__)
    #CZ#send_email._send()

        if not email_ongmail:
            send_email._setMailSmtp        (email__smtp__)
            send_email._setMailStartTLS    (emailStartTLS)
            send_email._setMailAuthUser    (emailAuthUser)
            send_email._setMailAuthPswd    (emailAuthPswd)
            send_email._setMailFrom        (email__from__)

        if args.verbose:
        #CZ#print('___________________')
        #CZ#print('|                 |')
        #CZ#print('| Send mail check |')
        #CZ#print('|_________________|________________________________________________________________________________')
            print('___________________________________________________________________________________________________')
            print('|')
            print('| ' + email__subj__)
            print('|__________________________________________________________________________________________________')
            print(email__body__)
            print('___________________________________________________________________________________________________')

        try:
        #CZ#send_email._verbose(args.verbose)
        #CZ#send_email._debug(args.debug)
            send_email._send()
        except:
            print("Send mail detect & check, but an error occurs!")
            raise(Exception(sys.exc_info()))
    else:
        print("Send mail detect, but not check!")

###############################################################################
#def _bytes2human_1(value):
#    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
#    prefix = {}
#    for i, s in enumerate(symbols):
#        prefix[s] = 1 << (i + 1) * 10
#    for s in reversed(symbols):
#        if value >= prefix[s]:
#            n = float(value) / prefix[s]
#            return '%.1f%s' % (n, s)
#    return '%sB' % value
###############################################################################
#def _bytes2human_2(value, suffix='B'):
#    unit_base = 1024.0
#    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z' ]:
#        if abs(value) < unit_base:
#            return '%3.1f%s%s' % (value, unit, suffix)
#        value /= unit_base
#    return '%.1f%s%s' % (value, 'Y', suffix)
###############################################################################
def _bytes2human(value):
    return(_bytes_human_manip.bytes2human(value))
###############################################################################
def _human2bytes(value):
    if value.isdigit():
        value = ('%sB' %value)
    return(_bytes_human_manip.human2bytes(value))

###############################################################################
def _getmount(path_base):
    path_base = os.path.normpath(path_base)
    path_base_split = path_base.split(os.sep)

    path_mount = path_base

    for i in range(0, len(path_base_split)):
        path_name = os.sep.join(path_base_split[0:i])
        if os.path.ismount(path_name):
            path_mount = path_name

    return(path_mount)

###############################################################################
def _replaces(string, _path_base=''):
    string = string.replace('$path_base$', _path_base);
    string = string.replace('$host_type$', _os_host_type);
    string = string.replace('$host_name$', _os_host_name);
    return(string)

###############################################################################
def _getargs():
#CZ#parser = argparse.ArgumentParser(description=_description, epilog=_epilog, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=120)
    formatter = lambda prog: argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=50, width=120)
    formatter = lambda prog: argparse.RawDescriptionHelpFormatter(prog, max_help_position=50, width=120)
    parser = argparse.ArgumentParser(description=_description, epilog=_epilog, formatter_class=formatter) #, argument_default=not argparse.SUPPRESS)

#CZ#pgroup.add_argument('-p' , '--power'       , help='display a power of a given number'    , type=int           , choices=[1,2,3,4,5])
#CZ#pgroup.add_argument('-s' , '--square'      , help='display a square of a given number'   , type=int)
    parser.add_argument('-d' , '--debug'       , help='increase output debug'                , action='count'     , default=0)
    parser.add_argument('-v' , '--verbose'     , help='output verbosity'                     , action='store_true')
    parser.add_argument('-V' , '--version'     , help='print version number'                 , action='version'   , version='%(prog)s '+_version)
    parser.add_argument('-pb', '--path_base'   , help='path base or set path this script'    , type=str)
    parser.add_argument('-lf', '--limit_free'  , help='limit space free'                     , type=str           , required=True)
    parser.add_argument('-hv', '--human_value' , help='return human values instead of byte'  , action='store_true')
    parser.add_argument('-sm', '--send_mail'   , help='send mail notification'               , action='store_true')
    parser.add_argument('-gm', '--gmail'       , help='set Gmail SMTP'                       , action='store_true')
    parser.add_argument('-mh', '--mail_host'   , help='mail host SMTP (default: %(default)s)', type=str           , default=_mail_host)
    parser.add_argument('-mf', '--mail_from'   , help='mail from (default: %(default)s)'     , type=str           , default=_mail_from)
    parser.add_argument('-mt', '--mail_to'     , help='mail to'                              , type=str           , required=True)
    parser.add_argument('-mc', '--mail_cc'     , help='mail cc'                              , type=str)
    parser.add_argument('-ms', '--mail_subject', help='mail subject (default: %(default)s)'  , type=str           , default=_mail_subject)
    parser.add_argument('-mm', '--mail_message', help='mail message'                         , type=str)
#CZ#parser.add_argument('name'                 , help='Name')
#CZ#parser.add_argument('surname'              , help='Surnamename')

    args = parser.parse_args()

    return(args)

###############################################################################
if __name__ == '__main__':
    exit = None
    args = _getargs()

    path_base = args.path_base
    if path_base is None:
        path_base = os.getcwd()
    path_base = _getmount(path_base)

    (space_b_total
    ,space_b_used
    ,space_b_free) = _os_disk._disk_usage(path_base)

    space_h_total = space_b_total
    space_h_used  = space_b_used
    space_h_free  = space_b_free
    if args.human_value:
        space_h_total = _bytes2human(space_h_total)
        space_h_used  = _bytes2human(space_h_used)
        space_h_free  = _bytes2human(space_h_free)

    message_print = _mail_message % (path_base, space_h_total, space_h_used, space_h_free)
    print(message_print)

    limit_b_free = _human2bytes(args.limit_free)
    limit_h_free = limit_b_free
    if args.human_value:
        limit_h_free = _bytes2human(limit_h_free)

    if space_b_free <= limit_b_free:
        message_alert = _message_alert  % limit_h_free
        print(message_alert)
        exit = 1

        _sendmail(_sendmail_prepare(args, message_print, message_alert))
    else:
        _message_allok = _message_allok  % limit_h_free
        print(_message_allok)
        exit = 0

    sys.exit(exit)