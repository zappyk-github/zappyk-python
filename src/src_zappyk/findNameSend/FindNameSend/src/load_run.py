# -*- coding: utf-8 -*-
__author__ = 'zappyk'

from lib_zappyk._email   import _email
from lib_zappyk._os_file import _nameListDir
from lib_zappyk._string  import _removeFirstEmptyLine, _stringToList, _search

from findNameSend.FindNameSend.cfg.load_cfg  import parser_args, parser_conf, logger_conf
from findNameSend.FindNameSend.cfg.load_ini  import *
from findNameSend.FindNameSend.src.constants import *

args = parser_args().args
conf = parser_conf().conf
logs = logger_conf().logs

tag_path_base = conf.get       ("ConfigPaths", "tag_path_base", fallback=tag_path_base)
tag_path_last = conf.get       ("ConfigPaths", "tag_path_last", fallback=tag_path_last)
end_grep_regx = conf.get       ("ConfigPaths", "end_grep_regx", fallback=end_grep_regx)
end_grep_ifno = conf.get       ("ConfigPaths", "end_grep_ifno", fallback=end_grep_ifno)
end_line_back = conf.getint    ("ConfigPaths", "end_line_back", fallback=end_line_back)
tag_name_exte = conf.get       ("ConfigPaths", "tag_name_exte", fallback=tag_name_exte)
tag_name_regx = conf.get       ("ConfigPaths", "tag_name_regx", fallback=tag_name_regx)
tag_grep_regx = conf.get       ("ConfigPaths", "tag_grep_regx", fallback=tag_grep_regx)
tag_line_regx = conf.get       ("ConfigPaths", "tag_line_regx", fallback=tag_line_regx)
tag_line_init = conf.getint    ("ConfigPaths", "tag_line_init", fallback=tag_line_init)
tag_line_done = conf.getint    ("ConfigPaths", "tag_line_done", fallback=tag_line_done)
tag_find_last = conf.getboolean("ConfigPaths", "tag_find_last", fallback=tag_find_last)
tag_path_find = conf.get       ("SearchPaths", "tag_path_find", fallback=tag_path_find)
tag_path_find = _removeFirstEmptyLine(tag_path_find)
tag_path_find = _stringToList(tag_path_find)
tag_path_desc = conf.get       ("SearchPaths", "tag_path_desc", fallback=tag_path_desc)
tag_path_desc = _removeFirstEmptyLine(tag_path_desc)
tag_path_desc = _stringToList(tag_path_desc)

email_notify_ = conf.getboolean("SendMail"   , "email_notify_", fallback=email_notify_)
email__smtp__ = conf.get       ("SendMail"   , "email__smtp__", fallback=email__smtp__)
email__from__ = conf.get       ("SendMail"   , "email__from__", fallback=email__from__)
email___to___ = conf.get       ("SendMail"   , "email___to___", fallback=email___to___)
email___cc___ = conf.get       ("SendMail"   , "email___cc___", fallback=email___cc___)
email___ccn__ = conf.get       ("SendMail"   , "email___ccn__", fallback=email___ccn__)
email_attachs = conf.get       ("SendMail"   , "email_attachs", fallback=email_attachs)
email_attachs = _removeFirstEmptyLine(email_attachs)
email_subject = conf.get       ("SendMail"   , "email_subject", fallback=email_subject)
email_message = conf.get       ("SendMail"   , "email_message", fallback=email_message)
email_message = _removeFirstEmptyLine(email_message)
emailfontsize = conf.get       ("SendMail"   , "emailfontsize", fallback=emailfontsize)

email___to___ = _stringToList(email___to___, ' ')
email___cc___ = _stringToList(email___cc___, ' ')
email___ccn__ = _stringToList(email___ccn__, ' ')
email_attachs = _stringToList(email_attachs)

if args.not_send_email:
    email_notify_ = False

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

    #CZ#for path_find in tag_path_find:
        for i in range(len(tag_path_find)):
            path_find = tag_path_find[i]
            path_desc = tag_path_desc[i]

            if args.verbose:
                logs.info(LINE_SEPARATOR)
                logs.info("Read path: [%s]" % path_find)

        #CZ#list_last = get_list_last_name_regx(path_find)
            list_last = get_list_last_name_exte(path_find)

            if args.verbose and tag_find_last:
                file_last = None
                if list_last:
                    file_last = list_last[0]
                logs.info("Last file: [%s]" % file_last)

            for file_last in list_last:
                name_last = os.path.basename(file_last)
            #CZ#row_error = get_row_error_line(file_last)
            #CZ#row_error = get_row_error_range(file_last)
                row_error = get_row_error_range(file_last, tag_line_init, tag_line_done)

                if row_error != '':
                    logs.info("____________________________")
                #CZ#logs.info("Trovate linee con errori in: %s" % name_last)
                    logs.info("Intercettati errori in file: %s" % name_last)

                    if args.debug >=1:
                        logs.info("Row error:\n%s" % row_error, end='')

                    if email_notify_:
                        try:
                            email__subj__ = email_subject % (path_desc)
                            email__body__ = email_message % (name_last
                                                            ,path_desc
                                                            ,row_error)

                            logs.info("Invio notifica email in corso...")
                            send_email._setMailSubject(email__subj__)
                            send_email._setMailMessage(email__body__)
                            send_email._setMailAttachs([file_last])
                            send_email._send()
                            logs.info("Invio notifica email completata!")
                        except:
                            logs.info("Invio notifica email con errori! :-(")
                            exc_type, exc_value, exc_traceback = sys.exc_info()
                            logs.traceback(exc_traceback)
                            logs.warning(exc_value)
                    else:
                        logs.info("Invio notifica email disabilitata. :-|")
                else:
                #CZ#logs.info("____________________________")
                    logs.info("Nessuna linea con errori in: %s" % name_last)

    except:
        logs.warning("(*** USCITA ANOMALA ***) o_O")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logs.traceback(exc_traceback)
        logs.error(exc_value)

    sys.exit(0)

###############################################################################
def get_list_last_name_regx(path_find):
    list_last = []
    time_last = 0

#CZ#for file_find in _os_file._fileListDir(path_find):
    for name_find in _nameListDir(path_find):
        if _search(tag_name_regx, name_find):
            file_find = path_find + name_find
            if args.debug >=1: logs.info("Read file: [%s]" % file_find)

            if tag_find_last:
                # read time file creation
            #CZ#sta_time = os.stat(file_find).st_atime # st_atime = time of most recent access
                stm_time = os.stat(file_find).st_mtime # st_mtime = time of most recent content modification
            #CZ#stc_time = os.stat(file_find).st_ctime # st_ctime = platform dependent: time of most recent metadata change on Unix,
                                                       #                         or the time of creation on Windows

                # get max time
                max_time = 0
            #CZ#if sta_time > max_time:
            #CZ#    max_time = sta_time
                if stm_time > max_time:
                    max_time = stm_time
            #CZ#if stc_time > max_time:
            #CZ#    max_time = stc_time

                # get max file
                if max_time > time_last:
                    if len(list_last) == 0:
                        list_last.append(file_find)
                    else:
                        list_last[0] = file_find
                    time_last = max_time
            else:
                list_last.append(file_find)

    return(list_last)

###############################################################################
def get_list_last_name_exte(path_find):
    list_last = []

    import glob

#CZ#file_find = max(glob.iglob(os.path.join(path_find, tag_name_exte)), key=os.path.getatime)
    file_find = max(glob.iglob(os.path.join(path_find, tag_name_exte)), key=os.path.getmtime)
#CZ#file_find = max(glob.iglob(os.path.join(path_find, tag_name_exte)), key=os.path.getctime)

    list_last.append(file_find)

    return(list_last)

###############################################################################
def get_row_error_range(file_last, line_range_init=0, line_range_done=1):
    line_find = []
    line_read = []

    with open_file(file_last) as file:
        line_read = file.readlines()
        file.close()

    okif_regx = False
    for i in range(0, len(line_read)):
        line = line_read[i]
        if args.debug >=3: logs.info("Line file: [%s" % line, end='')

        if _search(end_grep_regx, line):
            if args.debug >=2: logs.info("Find tag_okif_regex=[%s]" % end_grep_regx)
            okif_regx = True

        if _search(tag_grep_regx, line):
            if args.debug >=2: logs.info("Line find: [%s" % line, end='')

        #CZ#line_find.append(line)
            if _search(tag_line_regx, line):
                line_list = get_line_range(i, line_range_init, line_range_done, line_read)
                line_find.extend(line_list)
            else:
            #CZ#line_find.append(line)
            #CZ#line_list = get_line_range(i, line_range_init)
                line_list = get_line_range(i, line_range_init, 0)
                line_find.extend(line_list)

    if not okif_regx:
        line_list = get_line_range(len(line_read)-end_line_back, 0, end_line_back, line_read)
        line_find.extend(line_list)
        line_find.extend("\n")
        line_find.extend(end_grep_ifno)

    row_error = ''.join(line_find)

    return(row_error)

###############################################################################
def get_line_range(line_start, line_range_init=0, line_range_done=1, line_read=[]):
    line_find = []
    line_init = line_start + line_range_init
    line_done = line_start + line_range_done

    line_range = line_range_done - line_range_init
    if line_range <= 0:
        line_range = 1
        line_init = line_start
        line_done = line_start + line_range

    if line_init < 0:
        line_init = 0
    if line_done > len(line_read):
        line_done = len(line_read)

    for i in range(line_init, line_done):
        line = line_read[i]
        line = "Row #%-5s|%s" % (i, line)

        line_find.append(line)

#CZ#if   line_range > 1:
    if ((line_range > 1) and (line_range_done > 0)):
        line_find.append(LINE_BOX_BRECK + "\n")

    return(line_find)

###############################################################################
def get_row_error_line(file_last):
    line_find = []

    with open_file(file_last) as file:
        for line in file:
            if args.debug >=2: logs.info("Line file: [%s" % line, end='')

            if _search(tag_grep_regx, line):
                if args.debug >=1: logs.info("Line find: [%s" % line, end='')

                line_find.append(line)

        file.close()

    row_error = ''.join(line_find)

    return(row_error)

###############################################################################
def open_file(file):
#CZ#return(open(file))
#CZ#return(open(file, 'r', encoding="ascii"     , errors="surrogateescape"))
#CZ#return(open(file, 'r', encoding="ascii"     , errors="replace"))
#CZ#return(open(file, 'r', encoding="utf-8"     , errors="replace"))
    return(open(file, 'r', encoding="iso-8859-1", errors="replace"))
