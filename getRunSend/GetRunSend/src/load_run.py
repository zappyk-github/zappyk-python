# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys

from time    import sleep
from filecmp import cmp

from lib_zappyk._email   import _email
from lib_zappyk._os      import _os
from lib_zappyk._os_file import _os_file
from lib_zappyk._string  import _string
from lib_zappyk._wget    import _wget

from GetRunSend.cfg.load_cfg import parser_args, parser_conf, logger_conf
from GetRunSend.cfg.load_ini import *

args = parser_args().args
conf = parser_conf().conf
logs = logger_conf().logs

tag_file_name = conf.get       ("GetFile"   , "tag_file_name", fallback=tag_file_name)
tag_down_path = conf.get       ("GetFile"   , "tag_down_path", fallback=tag_down_path)
tag_down_name = conf.get       ("GetFile"   , "tag_down_name", fallback=tag_down_name)
tag_load_path = conf.get       ("GetFile"   , "tag_load_path", fallback=tag_load_path)
tag_load_name = conf.get       ("GetFile"   , "tag_load_name", fallback=tag_load_name)

url_path_name = conf.get       ("UrlFile"   , "url_path_name", fallback=url_path_name)
url_file_name = conf.get       ("UrlFile"   , "url_file_name", fallback=url_file_name)
url_path_file = conf.get       ("UrlFile"   , "url_path_file", fallback=url_path_file)

commands_exec = conf.getboolean("RunCommand", "commands_exec", fallback=commands_exec)
commands_open = conf.get       ("RunCommand", "commands_open", fallback=commands_open)
time_for_loop = conf.getint    ("RunCommand", "time_for_loop", fallback=time_for_loop)

email_notify_ = conf.getboolean("SendMail"  , "email_notify_", fallback=email_notify_)
email__smtp__ = conf.get       ("SendMail"  , "email__smtp__", fallback=email__smtp__)
email__from__ = conf.get       ("SendMail"  , "email__from__", fallback=email__from__)
email___to___ = conf.get       ("SendMail"  , "email___to___", fallback=email___to___)
email___cc___ = conf.get       ("SendMail"  , "email___cc___", fallback=email___cc___)
email___ccn__ = conf.get       ("SendMail"  , "email___ccn__", fallback=email___ccn__)
email_attachs = conf.get       ("SendMail"  , "email_attachs", fallback=email_attachs)
email_attachs = _string._removeFirstEmptyLine(email_attachs)
email_subject = conf.get       ("SendMail"  , "email_subject", fallback=email_subject)
email_message = conf.get       ("SendMail"  , "email_message", fallback=email_message)
email_message = _string._removeFirstEmptyLine(email_message)
emailfontsize = conf.get       ("SendMail"  , "emailfontsize", fallback=emailfontsize)

email___to___ = _string._stringToList(email___to___, ' ')
email___cc___ = _string._stringToList(email___cc___, ' ')
email___ccn__ = _string._stringToList(email___ccn__, ' ')
email_attachs = _string._stringToList(email_attachs)

###############################################################################
def main():
    try:
        send_email = _email()
        send_email._setMailSmtp        (email__smtp__)
        send_email._setMailAuthUser    (emailAuthUser)
        send_email._setMailAuthPswd    (emailAuthPswd)
        send_email._setMailSubject     (email_subject)
    #CZ#send_email._setMailMessage     (email_message)
        send_email._setMailFrom        (email__from__)
        send_email._setMailTo          (email___to___)
        send_email._setMailCc          (email___cc___)
        send_email._setMailCcn         (email___ccn__)
        send_email._setMailHtmlFontSize(emailfontsize)

        loop_count = 1
        while (True):
            _os._clear()

            tag_on_log = "|%05s|" % (loop_count)
            logs.info("%s========================================================================" % (tag_on_log))

            try:
                logs.info("%s Scarico file %s in corso..." % (tag_on_log, url_file_name))
                _wget._wgetFile(url_path_file, tag_down_name)
                logs.info("%s Scarico file %s completato!" % (tag_on_log, url_file_name))
            except:
                logs.info("(*** USCITA MENTRE SCARICAVO IL FILE ***) *_*")
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logs.traceback(exc_traceback)
                logs.error(exc_value)

            load_file = True
            if _os_file._fileExist(tag_load_name):
                logs.info("%s Confronto file %s => %s in corso..." % (tag_on_log, tag_down_name, tag_load_name))
                load_file = not cmp(tag_down_name, tag_load_name)
                logs.info("%s Confronto file %s => %s completato!" % (tag_on_log, tag_down_name, tag_load_name))

                if load_file:
                    logs.info("%s I files sembrano diversi, procedo con il caricamento... :-|" % (tag_on_log))
                else:
                    logs.info("%s I files sembrano uguali :-)" % (tag_on_log))
            else:
                logs.info("%s Copio file %s => %s in corso..." % (tag_on_log, tag_down_name, tag_load_name))
                _os_file._copy2(tag_down_name, tag_load_name)
                logs.info("%s Copio file %s => %s completato!" % (tag_on_log, tag_down_name, tag_load_name))

            if load_file:
                commands_exit = 0
                commands_logs = ''

                if commands_exec:
                    return_code = 0
                    return_stdo = ''
                    return_stde = ''

                    try:
                        logs.info("%s Esecuzione comando [%s] in corso..." % (tag_on_log, commands_open))
                    #CZ#(return_code) = _os._system(commands_open)
                        (return_code
                        ,return_stdo
                        ,return_stde) = _os._popen(commands_open)
                        logs.info("%s Esecuzione comando [%s] completato!" % (tag_on_log, commands_open))
                    except:
                        logs.info("%s Esecuzione comando [%s] con errori! :-(" % (tag_on_log, commands_open))
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        return_code = 1
                        return_stde = str(exc_value)
                        logs.traceback(exc_traceback)
                        logs.warning(exc_value)
                    #CZ#logs.error(exc_value)

                    commands_exit = return_code
                    if return_stdo != '':
                        commands_logs = "\n".join((commands_logs, return_stdo))
                    if return_stde != '':
                        commands_logs = "\n".join((commands_logs, return_stde))
                else:
                    logs.info("%s Esecuzione %s disabilitata. :-|" % (tag_on_log, commands_open))

                ###############################################################
                '''
                logs.warning("return_code: %s" % return_code)
                logs.warning("return_stdo: %s" % return_stdo)
                logs.warning("return_stde: %s" % return_stde)
                sys.exit(0)
                #
                mail__body__ = email_message % (commands_logs
                                               ,commands_exit
                                               ,'<file.read()>')
                logs.warning(mail__body__)
                sys.exit(0)
                '''
                ###############################################################

                email_notify_ = False
                if email_notify_:
                    try:
                        with open(tag_load_name) as file:
                            email__body__ = email_message % (commands_logs
                                                            ,commands_exit
                                                            ,file.read())
                            file.close()

                        logs.info("%s Invio notifica email in corso..." % (tag_on_log))
                        send_email._setMailMessage(email__body__)
                        send_email._send()
                        logs.info("%s Invio notifica email completata!" % (tag_on_log))
                    except:
                        logs.info("%s Invio notifica email con errori! :-(" % (tag_on_log))
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        logs.traceback(exc_traceback)
                        logs.warning(exc_value)
                else:
                    logs.info("%s Invio notifica email disabilitata. :-|" % (tag_on_log))

            try:
                logs.info("%s ...aspetto %s secondi..." % (tag_on_log, time_for_loop))
                sleep(time_for_loop)
                loop_count += 1
            except:
                logs.warning("(*** USCITA MENTRE ASPETTAVO ***) ^_*")
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logs.traceback(exc_traceback)
                logs.error(exc_value)

    except:
        logs.warning("(*** USCITA ANOMALA ***) o_O")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logs.traceback(exc_traceback)
        logs.error(exc_value)

    sys.exit(0)