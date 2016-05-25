#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'pes0zap'

import os, sys, html
import argparse #, configparser
import requests, hashlib
import zipfile

from lib_zappyk._os      import _os_host_type, _os_host_name
from lib_zappyk._os_file import _basename, _makeDir, _pathJoin, _fileExist, _fileMove, _fileRemove
from lib_zappyk._log     import _log
from lib_zappyk._date    import _dateNowFormat
from lib_zappyk._email   import _email
from lib_zappyk._string  import _findall

_version = '0.1'

_project = 'CurlUploader'

_description = '''
Simulate curl program for upload file.

Replace variables:
  *  $host_name$ with name host
  *  $host_type$ with type host
  *  $flow_user$ with flow user
  *  $path_file$ with path file
  *  $path_save$ with save path
'''

_epilog = "Version: %s" % _version

_http_detect_exitcode = '[[0]]'
_http_contents_decode = 'utf-8'
_http_tag_flowName    = 'flowName'
_http_tag_flowCPWD    = 'flowCPWD'
_http_tag_fileUpload  = 'fileUpload'
_save_tag_fileUpload  = '%Y%m%d_%H-%M.%S_'

_mail_message_sep = '''
_______________________________________________________________________________
'''

_mail_host    = 'smtp.payroll.it'
_mail_from    = 'it@payroll.it'
_mail_subject = 'WExeMFT: Alert, flow $flow_user$ uploader file on $host_name$ ($host_type$)'
_mail_message = """
Flow User = [<b>%s</b>]
Path File = [<b>%s</b>]
Path Save = [<b>%s</b>]
<i>WExeMFT on $host_name$ generate messagge:</i>
_______________________________________________________________________________

%s
_______________________________________________________________________________
"""

_message_error = 'Upload file "%s" failed error! :-('
_message_alert = 'Upload file "%s" is not found! :-|'
_message_butok = '%s\n\nBut something is failed! :-|\n\n%s'
_message_allok = 'Upload file "%s" successfully! :-)'

logs = _log()

###############################################################################
def _sendmail_prepare(args, message_email):

    if args.mail_message is not None:
        message_email.insert(0, _mail_message_sep)
        message_email.insert(0, args.mail_message)

    args.mail_message = "\n".join(message_email)

    args.mail_subject = _replaces(args.mail_subject, _flow_user=url_username, _path_save=path_save, _path_file=path_file)
    args.mail_message = _replaces(args.mail_message, _flow_user=url_username, _path_save=path_save, _path_file=path_file)

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
    email___to___ = [args.mail_to]
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

        send_email._setMailHtmlBodyEscape(False)

        if not email_ongmail:
            send_email._setMailSmtp        (email__smtp__)
            send_email._setMailStartTLS    (emailStartTLS)
            send_email._setMailAuthUser    (emailAuthUser)
            send_email._setMailAuthPswd    (emailAuthPswd)
            send_email._setMailFrom        (email__from__)

        if args.verbose:
        #CZ#logs.info('___________________')
        #CZ#logs.info('|                 |')
        #CZ#logs.info('| Send mail check |')
        #CZ#logs.info('|_________________|________________________________________________________________________________')
            logs.info('___________________________________________________________________________________________________')
            logs.info('|')
            logs.info('| ' + email__subj__)
            logs.info('|__________________________________________________________________________________________________')
            logs.info(email__body__)
            logs.info('___________________________________________________________________________________________________')

        try:
        #CZ#send_email._verbose(args.verbose)
        #CZ#send_email._debug(args.debug)
            send_email._send()
        except:
            logs.warning("Send mail detect & check, but an error occurs!")
            raise(Exception(sys.exc_info()))
    else:
        logs.warning("Send mail detect, but not check!")

###############################################################################
def _getmount(path_save):
    path_base = os.path.normpath(path_save)
    path_base_split = path_base.split(os.sep)

    path_mount = path_base

    for i in range(0, len(path_base_split)):
        path_name = os.sep.join(path_base_split[0:i])
        if os.path.ismount(path_name):
            path_mount = path_name

    return(path_mount)

###############################################################################
def _replaces(string, _flow_user='', _path_save='', _path_file=''):
    string = string.replace('$host_name$', _os_host_name);
    string = string.replace('$host_type$', _os_host_type);
    string = string.replace('$flow_user$', _flow_user);
    string = string.replace('$path_save$', _path_save);
    string = string.replace('$path_file$', _path_file);
    return(string)

###############################################################################
def _checkExitCode(message):
    exitcode = True

    if _findall(_http_detect_exitcode, message):
        exitcode = False

    return(exitcode)

###############################################################################
def _save_file(path_file, path_save, name_zip_):
    try:
        _makeDir(path_save)

        save_date = _dateNowFormat(_save_tag_fileUpload)
        name_save = '%s%s' % (save_date, _basename(path_file))
        file_save = _pathJoin([path_save, name_save])
        name_zip_ = '%s.zip' % name_zip_
        file_zip_ = _pathJoin([path_save, name_zip_])

        _fileMove(path_file, file_save)
    except:
        pass

    with zipfile.ZipFile(file_zip_, 'a') as zip:

        try:
            zip.write(file_save, _basename(file_save))
        except:
            pass
        finally:
            zip.close()

        _fileRemove(file_save)

###############################################################################
def _getargs():
#CZ#parser = argparse.ArgumentParser(description=_description, epilog=_epilog, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=120)
    formatter = lambda prog: argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=50, width=120)
    formatter = lambda prog: argparse.RawDescriptionHelpFormatter(prog, max_help_position=50, width=120)
    parser = argparse.ArgumentParser(description=_description, epilog=_epilog, formatter_class=formatter) #, argument_default=not argparse.SUPPRESS)

#CZ#pgroup.add_argument('-p' ,  '--power'       , help='display a power of a given number'    , type=int           , choices=[1,2,3,4,5])
#CZ#pgroup.add_argument('-s' ,  '--square'      , help='display a square of a given number'   , type=int)
    parser.add_argument('-d' ,  '--debug'       , help='increase output debug'                , action='count'     , default=0)
    parser.add_argument('-v' ,  '--verbose'     , help='output verbosity'                     , action='store_true')
    parser.add_argument('-V' ,  '--version'     , help='print version number'                 , action='version'   , version='%(prog)s '+_version)
    parser.add_argument('-ps',  '--path_save'   , help='path or save file uploader'           , type=str)
    parser.add_argument('-pf',  '--path_file'   , help='path file for uploader'               , type=str           , required=True)
    parser.add_argument('-ua',  '--url_address' , help='URL address for uploader file'        , type=str           , required=True)
    parser.add_argument('-uu',  '--url_username', help='URL authentication username'          , type=str           , required=True)
    parser.add_argument('-up',  '--url_password', help='URL authentication password'          , type=str           , required=True)
    parser.add_argument('-sm',  '--send_mail'   , help='send mail notification'               , action='store_true')
    parser.add_argument('-gm',  '--gmail'       , help='set Gmail SMTP'                       , action='store_true')
    parser.add_argument('-mh',  '--mail_host'   , help='mail host SMTP (default: %(default)s)', type=str           , default=_mail_host)
    parser.add_argument('-mf',  '--mail_from'   , help='mail from (default: %(default)s)'     , type=str           , default=_mail_from)
    parser.add_argument('-mt',  '--mail_to'     , help='mail to'                              , type=str           , required=True)
    parser.add_argument('-mc',  '--mail_cc'     , help='mail cc'                              , type=str)
    parser.add_argument('-ms',  '--mail_subject', help='mail subject (default: %(default)s)'  , type=str           , default=_mail_subject)
    parser.add_argument('-mm',  '--mail_message', help='mail message'                         , type=str)
#CZ#parser.add_argument('name'                  , help='Name')
#CZ#parser.add_argument('surname'               , help='Surnamename')

    args = parser.parse_args()

    return(args)

###############################################################################
if __name__ == '__main__':
    exit = None
    args = _getargs()

    path_save    = args.path_save
    path_file    = args.path_file
    url_address  = args.url_address
    url_username = args.url_username
    url_password = args.url_password
    url_pswd_md5 = hashlib.md5(url_password.encode()).hexdigest()

#CZ#if path_save is None:
#CZ#    path_save = os.getcwd()
#CZ#path_save = _getmount(path_save)

    exitcode = None
    messages = None

    if _fileExist(path_file):
        try:
            data_file = open(path_file, 'rb')

            from requests.auth import HTTPDigestAuth

            addr = url_address
            auth = HTTPDigestAuth(url_username, url_password)
            data = { _http_tag_flowName: url_username, _http_tag_flowCPWD: url_pswd_md5 }
            file = { _http_tag_fileUpload: data_file }

            response = requests.post(addr, auth=auth, data=data, files=file, allow_redirects=True)
            contents = response.content
            htmlpage = contents.decode(_http_contents_decode)
            messages = html.escape(htmlpage)
            exitcode = _checkExitCode(messages)

            data_file.close()

            if not exitcode:
                messages = _message_allok % path_file

                if path_save is not None:
                    _save_file(path_file, path_save, url_username)

                logs.info(messages)

        except Exception as e:
            exitcode = True
            if messages is None:
                messages = _message_error % path_file
            else:
                messages = _message_butok % (messages, str(e))
            logs.warning(messages)

    else:
        exitcode = False
        messages = _message_alert % path_file
        logs.warning(messages)

    if exitcode:
        message_email = _mail_message % (url_username, path_file, path_save, messages)
        logs.warning(message_email)

        _sendmail(_sendmail_prepare(args, [message_email]))

        exit = 1
    else:
        exit = 0

    sys.exit(exit)
