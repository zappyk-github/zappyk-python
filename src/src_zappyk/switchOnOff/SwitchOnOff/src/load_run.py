# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sqlite3

from lib_zappyk._email   import _email
from lib_zappyk._string  import _removeFirstEmptyLine, _stringToList

#CZ#from lib_external import mysql
from lib_external import pymysql
from lib_external import postgresql

from switchOnOff.SwitchOnOff.cfg.load_cfg  import parser_args, parser_conf, logger_conf
from switchOnOff.SwitchOnOff.cfg.load_ini  import *
from switchOnOff.SwitchOnOff.src.constants import *

args = parser_args().args
conf = parser_conf().conf
logs = logger_conf().logs

db_cnnct_type = conf.get       ("DbConnect", "db_cnnct_type", fallback=db_cnnct_type)
db_cnnct_host = conf.get       ("DbConnect", "db_cnnct_host", fallback=db_cnnct_host)
db_cnnct_user = conf.get       ("DbConnect", "db_cnnct_user", fallback=db_cnnct_user)
db_cnnct_pswd = conf.get       ("DbConnect", "db_cnnct_pswd", fallback=db_cnnct_pswd)
db_cnnct_name = conf.get       ("DbConnect", "db_cnnct_name", fallback=db_cnnct_name)

db_table_name = conf.get       ("DbTable"  , "db_table_name", fallback=db_table_name)
db_field_name = conf.get       ("DbTable"  , "db_field_name", fallback=db_field_name)
db_f_len_name = conf.getint    ("DbTable"  , "db_f_len_name", fallback=db_f_len_name)
db_field_desc = conf.get       ("DbTable"  , "db_field_desc", fallback=db_field_desc)
db_f_len_desc = conf.getint    ("DbTable"  , "db_f_len_desc", fallback=db_f_len_desc)
db_field_flag = conf.get       ("DbTable"  , "db_field_flag", fallback=db_field_flag)
db_f_len_flag = conf.getint    ("DbTable"  , "db_f_len_flag", fallback=db_f_len_flag)

db_sql_cancel = conf.get       ("DbQuery"  , "db_sql_cancel", fallback=db_sql_cancel)
db_sql_create = conf.get       ("DbQuery"  , "db_sql_create", fallback=db_sql_create)
db_sql_insert = conf.get       ("DbQuery"  , "db_sql_insert", fallback=db_sql_insert)
db_sql_delete = conf.get       ("DbQuery"  , "db_sql_delete", fallback=db_sql_delete)
db_sql_update = conf.get       ("DbQuery"  , "db_sql_update", fallback=db_sql_update)
db_sql_select = conf.get       ("DbQuery"  , "db_sql_select", fallback=db_sql_select)
db_sql__list_ = conf.get       ("DbQuery"  , "db_sql__list_", fallback=db_sql__list_)

email_notify_ = conf.getboolean("SendMail" , "email_notify_", fallback=email_notify_)
email__smtp__ = conf.get       ("SendMail" , "email__smtp__", fallback=email__smtp__)
email__from__ = conf.get       ("SendMail" , "email__from__", fallback=email__from__)
email___to___ = conf.get       ("SendMail" , "email___to___", fallback=email___to___)
email___cc___ = conf.get       ("SendMail" , "email___cc___", fallback=email___cc___)
email___ccn__ = conf.get       ("SendMail" , "email___ccn__", fallback=email___ccn__)
email_attachs = conf.get       ("SendMail" , "email_attachs", fallback=email_attachs)
email_attachs = _removeFirstEmptyLine(email_attachs)
email_subject = conf.get       ("SendMail" , "email_subject", fallback=email_subject)
email_message = conf.get       ("SendMail" , "email_message", fallback=email_message)
email_message = _removeFirstEmptyLine(email_message)
emailfontsize = conf.get       ("SendMail" , "emailfontsize", fallback=emailfontsize)

email___to___ = _stringToList(email___to___, ' ')
email___cc___ = _stringToList(email___cc___, ' ')
email___ccn__ = _stringToList(email___ccn__, ' ')
email_attachs = _stringToList(email_attachs)

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

        n_switch = 'switch'
        l_switch = db_f_len_flag
        l_switch = 3
        n_switch = n_switch[:l_switch]

        n_status = db_field_flag
        l_status = db_f_len_flag
        l_status = 1
        n_status = n_status[:l_status]

        row1head = '+-%s-+-%s-+-%s-+'      % (_ftc( db_f_len_name), _ftc( db_f_len_desc), _ftc(l_status))
        row2head = '| %s | %s | %s |'      % (_ftt(-db_f_len_name), _ftt(-db_f_len_desc), _ftt(l_status))
        row_line = '+-%s-+-%s-+-%s-+*%s**' % (_ftc( db_f_len_name), _ftc( db_f_len_desc), _ftc(l_status), _ftc(l_switch, '*'))
        row_body = '| %s | %s | %s | %s *' % (_ftt(-db_f_len_name), _ftt(-db_f_len_desc), _ftt(l_status), _ftt(l_switch))
        row_head = "\n".join([row_line
                             ,row_body % (db_field_name, db_field_desc, n_status, n_switch)
                             ,row_line])
        row_head = "\n".join([row1head
                             ,row2head % (db_field_name, db_field_desc, n_status)
                             ,row_line])

        db_cnt = None
        db_cur = None

        ###############
        #   SqlLite   #
###############################################################################
        if db_cnnct_type == DB_TYPE_SQLITE:
            conuri = db_cnnct_name
            config = db_cnnct_name
            try:
                if args.verbose:
                    logs.info('* DB %s connect to %s' % (db_cnnct_type, conuri))
                db_cnt = sqlite3.connect(config)
                db_cur = db_cnt.cursor()
                db_cur.row_factory = sqlite3.Row
                if args.verbose:
                    logs.info('* DB %s connected! :-)' % db_cnnct_type)
            except sqlite3.Error as e:
                logs.warning('* DB %s error:' % db_cnnct_type)
                logs.error(e)
            except:
                logs.warning('* DB %s generic error: :-(' % db_cnnct_type)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logs.traceback(exc_traceback)
                logs.error(exc_value)
        #CZ#else:
        #CZ#    logs.warning('* DB %s close' % db_cnnct_type)
        #CZ#    cnx.close()
###############################################################################

        ##################
        #   PostGreSql   #
###############################################################################
        if db_cnnct_type == DB_TYPE_POSTGRESQL:
            conuri = '%s@%s/%s' % (db_cnnct_name, db_cnnct_host, db_cnnct_name)
            config = 'pq://%s:%s@%s%s/%s' % (db_cnnct_user, db_cnnct_user, db_cnnct_host, '', db_cnnct_name)
            try:
                if args.verbose:
                    logs.info('* DB %s connect to %s' % (db_cnnct_type, conuri))
                db_cur = postgresql.open(config)
            #CZ#db_cur = db_cnt.cursor()
                if args.verbose:
                    logs.info('* DB %s connected! :-)' % db_cnnct_type)
            except:
                logs.warning('* DB %s generic error! :-(' % db_cnnct_type)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logs.traceback(exc_traceback)
                logs.error(exc_value)
        #CZ#else:
        #CZ#    logs.warning('* DB %s close' % db_cnnct_type)
        #CZ#    cnx.close()
###############################################################################

        #############
        #   MySql   #
###############################################################################
        if db_cnnct_type == DB_TYPE_MYSQL:
            conuri = '%s@%s/%s' % (db_cnnct_name, db_cnnct_host, db_cnnct_name)
            config = { 'host'     : db_cnnct_host
                     , 'user'     : db_cnnct_user
                     , 'password' : db_cnnct_pswd
                     , 'database' : db_cnnct_name }
            config = { 'host'     : db_cnnct_host
                     , 'user'     : db_cnnct_user
                     , 'passwd'   : db_cnnct_pswd
                     , 'db'       : db_cnnct_name }
            try:
                if args.verbose:
                    logs.info('* DB %s connect to %s' % (db_cnnct_type, conuri))
        #CZ#    db_cnt = mysql.connector.connect(**config)
        #CZ#    db_cur = db_cnt.cursor(cursor_class=mysql.MySQLCursorDict)
                db_cnt = pymysql.connect(**config)
                db_cur = db_cnt.cursor(pymysql.cursors.DictCursor)
                if args.verbose:
                    logs.info('* DB %s connected! :-)' % db_cnnct_type)
        #CZ#except mysql.connector.Error as e:
        #CZ#    if e.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
        #CZ#        logs.error("* DB %s error: something is wrong with your user name or password" % db_cnnct_type)
        #CZ#    elif e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        #CZ#        logs.error("* DB %s error: database does not exists" % db_cnnct_type)
        #CZ#    else:
        #CZ#        logs.warning('* DB %s error:' % db_cnnct_type)
        #CZ#        logs.error(e)
            except:
                logs.warning('* DB %s generic error! :-(' % db_cnnct_type)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logs.traceback(exc_traceback)
                logs.error(exc_value)
        #CZ#else:
        #CZ#    logs.warning('* DB %s close' % db_cnnct_type)
        #CZ#    cnx.close()
###############################################################################

        db_cmd = args.query
        db_sql = None
        db_bdy = None

        flag_query_cancel = True if db_cmd == DB_QUERY_CANCEL else False
        flag_query_create = True if db_cmd == DB_QUERY_CREATE else False
        flag_query__list_ = True if db_cmd == DB_QUERY__LIST_ else False
        flag_query_delete = True if db_cmd == DB_QUERY_DELETE else False
        flag_query_select = True if db_cmd == DB_QUERY_SELECT else False
        flag_query_update = True if db_cmd == DB_QUERY_UPDATE else False
        flag_query_insert = True if db_cmd == DB_QUERY_INSERT else False

        flag_notify_email = True if not (flag_query__list_ \
                                       or flag_query_select)  else False

        return_code = 0

        try:
###############################################################################
            if flag_query_cancel:
                db_sql = db_sql_cancel
                if args.verbose:
                    logs.info('* DB %s execute %s' % (db_cnnct_type, db_cmd))
                    logs.info('* DB %s query [%s]' % (db_cnnct_type, db_sql))
                db_cur.execute(db_sql)
                pass
            ###################################################################
            if flag_query_create:
                db_sql = db_sql_create
                if args.verbose:
                    logs.info('* DB %s execute %s' % (db_cnnct_type, db_cmd))
                    logs.info('* DB %s query [%s]' % (db_cnnct_type, db_sql))
                db_cur.execute(db_sql)
                pass
            ###################################################################
            if flag_query__list_:
                db_sql = db_sql__list_
                if args.verbose:
                    logs.info('* DB %s execute %s' % (db_cnnct_type, db_cmd))
                    logs.info('* DB %s query [%s]' % (db_cnnct_type, db_sql))
                if db_cnnct_type == DB_TYPE_POSTGRESQL:
                    rows = db_cur.prepare(db_sql)
                else:
                    db_cur.execute(db_sql)
                    rows = db_cur
                print(row_head)
                for row in rows:
                #CZ#line = (row[0], row[1], str(row[2])[:l_status], _flag_remap(row[2])
                    if db_cnnct_type == DB_TYPE_POSTGRESQL:
                        line = (            row[db_field_name.lower()]
                               ,            row[db_field_desc.lower()]
                               ,        str(row[db_field_flag.lower()])[:l_status]
                               ,_flag_remap(row[db_field_flag.lower()]))
                    else:
                        line = (            row[db_field_name]
                               ,            row[db_field_desc]
                               ,        str(row[db_field_flag])[:l_status]
                               ,_flag_remap(row[db_field_flag]))
                    print(row_body % line)
                print(row_line)
                pass
            ###################################################################
            if flag_query_delete:
                db_sql = db_sql_delete % (args.field_name)
                if args.verbose:
                    logs.info('* DB %s execute %s' % (db_cnnct_type, db_cmd))
                    logs.info('* DB %s query [%s]' % (db_cnnct_type, db_sql))
                db_cur.execute(db_sql)
                pass
            ###################################################################
            if flag_query_select:
                db_sql = db_sql_select % (args.field_name)
                if args.verbose:
                    logs.info('* DB %s execute %s' % (db_cnnct_type, db_cmd))
                    logs.info('* DB %s query [%s]' % (db_cnnct_type, db_sql))
                if db_cnnct_type == DB_TYPE_POSTGRESQL:
                    db_cur.prepare(db_sql)
                else:
                    db_cur.execute(db_sql)
                    rows = db_cur

                flag = None
                for row in rows:
                #CZ#flag = _flag_remap(row[0])
                    flag = _flag_remap(row[db_field_flag])
                #CZ#print('%s is %s (%s)' % (args.field_name, flag, row[0]))
                    print('%s is %s (%s)' % (args.field_name, flag, row[db_field_flag]))

                    if flag == FLAG_ON:
                        return_code = 0
                    if flag == FLAG_OFF:
                        return_code = 1

                    if args.is_on:
                        if flag == FLAG_ON:
                            return_code = 0
                        else:
                            return_code = 1
                    if args.is_off:
                        if flag == FLAG_OFF:
                            return_code = 0
                        else:
                            return_code = 1

                if flag is None:
                    return_code = 1
                pass
            ###################################################################
            if flag_query_update:
                db_sql = db_sql_update % (args.field_flag, args.field_name)
                if args.verbose:
                    logs.info('* DB %s execute %s' % (db_cnnct_type, db_cmd))
                    logs.info('* DB %s query [%s]' % (db_cnnct_type, db_sql))
                db_cur.execute(db_sql)
                pass
            ###################################################################
            if flag_query_insert:
                db_sql = db_sql_insert % (args.field_name, args.field_desc, args.field_flag)
                if args.verbose:
                    logs.info('* DB %s execute %s' % (db_cnnct_type, db_cmd))
                    logs.info('* DB %s query [%s]' % (db_cnnct_type, db_sql))
                db_cur.execute(db_sql)
                pass

###############################################################################
            if not flag_query_select:
                db_nty = True
                db_lst = []
                if db_cnnct_type == DB_TYPE_POSTGRESQL:
                    rows = db_cur.prepare(db_sql__list_)
                else:
                    db_cur.execute(db_sql__list_)
                    rows = db_cur
                db_lst.append(row_head)
                for row in rows:
                #CZ#line = (row[0], row[1], str(row[2])[:l_status], _flag_remap(row[2])
                    if db_cnnct_type == DB_TYPE_POSTGRESQL:
                        line = (            row[db_field_name.lower()]
                               ,            row[db_field_desc.lower()]
                               ,        str(row[db_field_flag.lower()])[:l_status]
                               ,_flag_remap(row[db_field_flag.lower()]))
                    else:
                        line = (            row[db_field_name]
                               ,            row[db_field_desc]
                               ,        str(row[db_field_flag])[:l_status]
                               ,_flag_remap(row[db_field_flag]))
                    db_lst.append(row_body % line)
                db_lst.append(row_line)
                db_bdy = "\n".join(db_lst)
                pass
###############################################################################
        except:
            logs.warning('* DB %s execute %s on error:' % (db_cnnct_type, db_cmd))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logs.traceback(exc_traceback)
            logs.error(exc_value)

        if db_cnnct_type == DB_TYPE_POSTGRESQL:
            pass
        else:
            db_cnt.commit()

        if db_cur:
            if args.verbose:
                logs.info('* DB %s close cursor' % db_cnnct_type)
            db_cur.close()
        if db_cnt:
            if args.verbose:
                logs.info('* DB %s close connect' % db_cnnct_type)
            db_cnt.close()

        #######################################################################
        if flag_notify_email:
            if email_notify_:
                send_email._verbose(False)
                try:
                    email__subj__ = email_subject % (db_cmd)
                    email__body__ = email_message % (db_sql
                                                    ,db_bdy)

                #CZ#logs.info("Invio notifica email in corso...")
                    send_email._setMailSubject(email__subj__)
                    send_email._setMailMessage(email__body__)
                    send_email._send()
                #CZ#logs.info("Invio notifica email completata!")
                except:
                #CZ#logs.info("Invio notifica email con errori! :-(")
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                #CZ#logs.warning(exc_value)
            else:
            #CZ#logs.info("Invio notifica email disabilitata. :-|")
                pass
        #######################################################################

    except:
        logs.warning("(*** USCITA ANOMALA ***) o_O")
        exc_type, exc_value, exc_traceback = sys.exc_info()
    #CZ#logs.traceback(exc_traceback)
        logs.error(exc_value)

    sys.exit(return_code)

###############################################################################
def _flag_remap(flag):
    mood = flag
    if type(flag) == bool:
        mood = FLAG_ON if flag else FLAG_OFF
    if type(flag) == int:
        mood = FLAG_ON if flag >= 1 else FLAG_OFF
    if type(flag) == str:
        mood = FLAG_ON if flag.strip.title == 'True' else FLAG_OFF
    return(mood)
###############################################################################
def _flag_remap_On(flag):
    mood = _flag_remap(flag)
    if mood == 'On':
        return(True)
    else:
        return(False)
###############################################################################
def _flag_remap_Off(flag):
    mood = _flag_remap(flag)
    if mood == 'Off':
        return(True)
    else:
        return(False)

###############################################################################
def _ftc(time=0, char='-'):
    return(char * int(time))
###############################################################################
def _ftt(time='', type='s'):
    return('%' + str(time) + type)