#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os, sys, html
import argparse #, configparser
import requests, hashlib
import zipfile

from lib_zappyk._os      import _os_host_type, _os_host_name
from lib_zappyk._os_file import _basename, _makeDir, _pathJoin, _fileExist, _fileMove, _fileRemove
from lib_zappyk._log     import _log
from lib_zappyk._date    import _dateNowFormat
from lib_zappyk._email   import _email
from lib_zappyk._string  import _findall, _crypting

_version = '0.1'

_project = 'CurlUploader'

_description = '''
Simulate curl program for upload file.

Replace variables:
  *  $host_name$ with name host
  *  $host_type$ with type host
  *  $flow_user$ with flow user
  *  $flow_name$ with flow_name
  *  $path_file$ with path file
  *  $path_save$ with save path
'''

_epilog = "Version: %s" % _version

_http_detect_exitcode = '[[0]]'
_http_contents_decode = 'utf-8'
_http_tag_flowName    = 'X-BOS-MFT-CLIENTID'
_http_tag_flowBosMft  = 'X-BOS-MFT'
_http_tag_fileUpload  = 'file'
_save_tag_fileUpload  = '%Y%m%d_%H-%M.%S_'
_code_key_crypting    = '1!S03r2v19c33s!8.!4P@8yr5017l!6'
_code_utf_codec       = 'utf-8'

_mail_message_sep = '''
_______________________________________________________________________________
'''

_mail_host    = 'smtp.payroll.it'
_mail_from    = 'admin@payroll.it'
_mail_to      = 'it@payroll.it'
_mail_subject = 'WExeMFT: Alert, flow $flow_name$ uploader file on $host_name$ ($host_type$)'
_mail_message = """
End Point = [<font color="red">%s</font>]
Flow User = [<font color="red">%s</font>]
Path File = [<font color="red">%s</font>]
Path Save = [<font color="red">%s</font>]
<i>WExeMFT on $host_name$ notify messagge:</i>
_______________________________________________________________________________

%s

--

​( Information Technology )
P&S Srl - Payroll Services
"""

_message_error = """Upload file "%s" failed error! :-("""
_message_moved = """Upload file "%s" is not moved! :-/"""
_message_check = """Detect file "%s" moved 4 send? :-@"""
_message_alert = """Upload file "%s" is not found! :-|"""
_message_butok = """%s\n\nBut something is failed! :-|\n\n%s"""
_message_allok = """Upload file "%s" successfully! :-)"""

logs = _log()
logs.setFormat('%Y%m%d %H:%M.%S| ')

###############################################################################
def _sendmail_prepare(args, message_email):

    if args.mail_message is not None:
        message_email.insert(0, _mail_message_sep)
        message_email.insert(0, args.mail_message)

    args.mail_message = "\n".join(message_email)

    args.mail_subject = _replaces(args.mail_subject, _flow_user=url_username, _flow_name=flow_name, _path_save=path_save, _path_file=path_file)
    args.mail_message = _replaces(args.mail_message, _flow_user=url_username, _flow_name=flow_name, _path_save=path_save, _path_file=path_file)

    if args.mail_to is None:
        args.mail_to = ''

    if args.mail_cc is None:
        args.mail_cc = ''

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
            send_email._setMailHtmlBodySend(False)
            logs.info("...email send true!")
        else:
            logs.info("...email send true, over Gmail!")

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
        except Exception as e:
            logs.warning("Send mail detect & check, but an error occurs!")
        #CZ#raise(Exception(sys.exc_info()))
            logs.warning(str(e))
            pass

    else:
        logs.warning("Send mail detect, but not check!")
'''
###############################################################################
def _getMount(path_save):
    path_base = os.path.normpath(path_save)
    path_base_split = path_base.split(os.sep)

    path_mount = path_base

    for i in range(0, len(path_base_split)):
        path_name = os.sep.join(path_base_split[0:i])
        if os.path.ismount(path_name):
            path_mount = path_name

    return(path_mount)
'''
###############################################################################
def _replaces(string, _flow_user='', _flow_name='', _path_save='', _path_file=''):
    string = string.replace('$host_name$', _os_host_name)
    string = string.replace('$host_type$', _os_host_type)
    string = string.replace('$flow_user$', _flow_user)
    string = string.replace('$flow_name$', _flow_name)
    string = string.replace('$path_save$', _path_save)
    string = string.replace('$path_file$', _path_file)
    return(string)

###############################################################################
def _checkExitCode(message):
    exitcode = True

    if _findall(_http_detect_exitcode, message):
        exitcode = False

    if message == '':
        exitcode = False

    return(exitcode)

###############################################################################
def _save_file(path_file, path_save, name_zip_):
    try:
        _makeDir(path_save)

        save_date = _dateNowFormat(_save_tag_fileUpload)
        name_save = '%s%s' % (save_date, _basename(path_file))
        file_save = _pathJoin([path_save, name_save])
        name_zip_ = '%s-bak.zip' % name_zip_
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
def _crypt(data, encode=False):
    return(_crypting(data, _code_key_crypting, _code_utf_codec, encode))

###############################################################################
def _getargs():
    _note_epilog = '''
Note: Proxy set environments   [ HTTP_PROXY | HTTPS_PROXY ]
         or set ref. options   [XXXX://[user:pass]@]host:port   where XXXX are [ http | https | socks5 | socks5h ]
      in this order of importance.

%s
''' % _epilog
#CZ#parser = argparse.ArgumentParser(description=_description, epilog=_epilog, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=120)
    formatter = lambda prog: argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=50, width=120)
    formatter = lambda prog: argparse.RawDescriptionHelpFormatter(prog, max_help_position=50, width=120)
#CZ#parser = argparse.ArgumentParser(description=_description, epilog=_epilog, formatter_class=formatter) #, argument_default=not argparse.SUPPRESS)
    parser = argparse.ArgumentParser(description=_description, epilog=_note_epilog, formatter_class=formatter)  # , argument_default=not argparse.SUPPRESS)

#CZ#pgroup.add_argument('-p' ,  '--power'          , help='display a power of a given number'    , type=int           , choices=[1,2,3,4,5])
#CZ#pgroup.add_argument('-s' ,  '--square'         , help='display a square of a given number'   , type=int)
    parser.add_argument('-d' ,  '--debug'          , help='increase output debug'                , action='count'     , default=0)
    parser.add_argument('-v' ,  '--verbose'        , help='output verbosity'                     , action='store_true')
    parser.add_argument('-V' ,  '--version'        , help='print version number'                 , action='version'   , version='%(prog)s '+_version)
    parser.add_argument('-ps',  '--path_save'      , help='path or save file uploader'           , type=str)
    parser.add_argument('-pf',  '--path_file'      , help='path file for uploader'               , type=str           , required=True)
    parser.add_argument('-fn',  '--flow_name'      , help='flow name for uploader'               , type=str           , required=True)
    parser.add_argument('-uph', '--url_proxy_http' , help='URL set proxy http'                   , type=str)
    parser.add_argument('-uphs','--url_proxy_https', help='URL set proxy https'                  , type=str)
    parser.add_argument('-ua',  '--url_address'    , help='URL address for uploader file'        , type=str           , required=True)
    parser.add_argument('-uu',  '--url_username'   , help='URL authentication username'          , type=str           , required=True)
    parser.add_argument('-up',  '--url_password'   , help='URL authentication password'          , type=str           , required=True)
    parser.add_argument('-cp',  '--cryptpswd'      , help='return crypted URL_PASSWORD'          , action='store_true')
    parser.add_argument('-sm',  '--send_mail'      , help='send mail notification'               , action='store_true')
    parser.add_argument('-gm',  '--gmail'          , help='set Gmail SMTP'                       , action='store_true')
    parser.add_argument('-mh',  '--mail_host'      , help='mail host SMTP (default: %(default)s)', type=str           , default=_mail_host)
    parser.add_argument('-mf',  '--mail_from'      , help='mail from (default: %(default)s)'     , type=str           , default=_mail_from)
    parser.add_argument('-mt',  '--mail_to'        , help='mail to (default: %(default)s)'       , type=str           , default=_mail_from)
    parser.add_argument('-mc',  '--mail_cc'        , help='mail cc'                              , type=str)
    parser.add_argument('-ms',  '--mail_subject'   , help='mail subject (default: %(default)s)'  , type=str           , default=_mail_subject)
    parser.add_argument('-mm',  '--mail_message'   , help='mail message'                         , type=str)
#CZ#parser.add_argument('name'                     , help='Name')
#CZ#parser.add_argument('surname'                  , help='Surname')

    args = parser.parse_args()

    return(args)

###############################################################################
if __name__ == '__main__':
    exit = None
    args = _getargs()

    path_save    = args.path_save
    path_file    = args.path_file
    flow_name    = args.flow_name
    cryptpswd    = args.cryptpswd
    url_address  = args.url_address
    url_username = args.url_username
#CZ#url_password = args.url_password
#CZ#url_pswd_md5 = hashlib.md5(url_password.encode()).hexdigest()
    url_pswd_md5 = args.url_password
#CZ#url_password = hashlib.md5(url_pswd_md5.encode()).hexdigest()
#CZ#url_password = hashlib.md5(url_pswd_md5.encode()).digest()
    url_password = None
    flow_bos_mft = '1'

    if cryptpswd:
        logs.error('%s : [%s]== crypted >>[%s]' % (flow_name, url_pswd_md5, _crypt(url_pswd_md5, encode=True)))
    else:
        try:
            url_password = _crypt(url_pswd_md5)
        except Exception as e:
        #CZ#logs.warning(str(e))
            logs.error("Password [%s] is crypted?" % url_pswd_md5)
    '''
    if path_save is None:
        path_save = os.getcwd()
    path_save = _getMount(path_save)
    '''
#_______________________________________________________________________________________________________________________________________________________________
#                                                                                                                                                              #
# curl --digest -u "url_username:url_password" -F "file=@path_file" -H "X-BOS-MFT=1" -H "X-BOS-MFT-CLIENTID=flow_name" url_address                             #
# curl          -u "url_username:url_password" -F "file=@path_file" -H "X-BOS-MFT=1" -H "X-BOS-MFT-CLIENTID=flow_name" url_address                             #
#______________________________________________________________________________________________________________________________________________________________#
#                                                                                                                                                              #
# curl          -u "%MFT_auth%"      -F "file=@%MFT_file%"     -H "X-BOS-MFT:1" -H "X-BOS-MFT-CLIENTID:%MFT_flow%" "%MFT_endp%"                                #
# curl          -u "tstmft0:tstmft0" -F "file=@C:\tmp\TST.txt" -H "X-BOS-MFT:1" -H "X-BOS-MFT-CLIENTID:TSTMFT0"    "http://apps.payroll.it/bos-mft-server/mft" #
#______________________________________________________________________________________________________________________________________________________________#

    exitcode = None
    messages = None

    move_file = None
    send_file = _pathJoin([path_save, ('%s_send2payroll_%s' % (flow_name, _basename(path_file)))])

    if _fileExist(send_file):
        move_file = send_file

        messages = (_message_check % send_file)
        logs.info(messages)
    else:
        if _fileExist(path_file):
            try:
                _fileMove(path_file, send_file)
                move_file = path_file
            except Exception as e:
                exitcode = True
                messages = _message_moved % path_file
                logs.warning(messages)

#CZ#if _fileExist(path_file):
#CZ#if _fileExist(send_file):
    if move_file is not None:
        try:
        #CZ#data_file = open(path_file, 'rb')
            data_file = open(send_file, 'rb')

        #CZ#from requests.auth import HTTPDigestAuth
            from requests.auth import HTTPBasicAuth

            addr = url_address
        #CZ#auth = HTTPDigestAuth(url_username, url_password)
            auth = HTTPBasicAuth(url_username, url_password)
            data = { }
            file = { _http_tag_fileUpload: data_file }
            head = { _http_tag_flowName: flow_name, _http_tag_flowBosMft: flow_bos_mft }

            '''
            proxies = {
                'http' : 'http://user:pass@host:port',
                'https': 'https://user:pass@host:port',
                'http' : 'socks5://user:pass@host:port',
                'https': 'socks5://user:pass@host:port',
                'http' : 'socks5h://user:pass@host:port',
                'https': 'socks5h://user:pass@host:port',
            }
            response = requests.post(addr, auth=auth, data=data, files=file, headers=head, allow_redirects=True, proxies=proxies)
            '''
            proxies = {}
            if os.getenv('HTTP_PROXY')  is not None: proxies['http']  = os.environ['HTTP_PROXY']
            if os.getenv("HTTPS_PROXY") is not None: proxies['https'] = os.environ['HTTPS_PROXY']
            if args.url_proxy_http      is not None: proxies['http']  = args.url_proxy_http
            if args.url_proxy_https     is not None: proxies['https'] = args.url_proxy_https

        #CZ#response = requests.post(addr, auth=auth, data=data, files=file, headers=head, allow_redirects=True)
            response = requests.post(addr, auth=auth, data=data, files=file, headers=head, allow_redirects=True, proxies=proxies)
            contents = response.content
            htmlpage = contents.decode(_http_contents_decode)
            exitcode = _checkExitCode(htmlpage)

        #CZ#messages = """<body style="border: 3px solid red;">%s</body>""" % html.escape(htmlpage)
            messages = """<body style="border: 3px solid red;">%s</body>""" % htmlpage

            data_file.close()

            if not exitcode:
            #CZ#messages = _message_allok % path_file
                messages = _message_allok % move_file

                if path_save is not None:
                #CZ#_save_file(path_file, path_save, flow_name)
                    _save_file(send_file, path_save, flow_name)

                logs.info(messages)

        except Exception as e:
            exitcode = True
            if messages is None:
            #CZ#messages = _message_error % path_file
                messages = _message_error % move_file
            else:
                messages = _message_butok % (messages, str(e))
            logs.warning(messages)

    else:
        if exitcode is None:
            exitcode = False
            messages = _message_alert % path_file
            logs.warning(messages)

    if exitcode:
    #CZ#message_email = _mail_message % (url_address, url_username, path_file, path_save, messages)
        message_email = _mail_message % (url_address, url_username, move_file, path_save, messages)
        logs.warning(message_email)

        _sendmail(_sendmail_prepare(args, [message_email]))

        exit = 1
    else:
        exit = 0

    sys.exit(exit)
