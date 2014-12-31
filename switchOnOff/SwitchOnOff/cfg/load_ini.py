# -*- coding: utf-8 -*-
import os, sys
###############################################################################
_Os_path_join = os.path.sep
###############################################################################
db_cnnct_type = 'SqLite'
db_cnnct_name = ':memory:'
db_cnnct_name = 'SwitchOnOff-database.sqlite'
db_cnnct_list = 'SEMAPHORE'
#==============================================================================
db_cnnct_type = 'PostGreSql'
db_cnnct_host = 'postgres.payroll.local'
db_cnnct_user = 'easy'
db_cnnct_pswd = 'easy'
db_cnnct_name = 'easyweb_p'
db_cnnct_list = 'SEMAPHORE'
#==============================================================================
db_cnnct_type = 'MySql'
db_cnnct_host = 'sql4.freemysqlhosting.net'
db_cnnct_user = 'sql435123'
db_cnnct_pswd = 'jM9*bV1*'
db_cnnct_name = 'sql435123'
db_cnnct_list = 'SEMAPHORE'
#------------------------------------------------------------------------------
db_cnnct_type = 'MySql'
db_cnnct_host = 'mysql.payroll.local'
db_cnnct_user = 'geroot'
db_cnnct_pswd = 'ger00t'
db_cnnct_name = 'MASTER'
db_cnnct_list = 'SEMAFORI'
###############################################################################
db_table_name = db_cnnct_list
#==============================================================================
db_field_name = 'NAME'
db_f_len_name = 15
db_field_desc = 'DESCRIPTION'
db_f_len_desc = 50
db_field_flag = 'STATUS'
db_f_len_flag = 6
###############################################################################
db_tag_cancel = "drop table %s"
db_tag_create = "create table %s (%s varchar(%s) not null primary key, %s varchar(%s), %s integer(1))"
db_tag__list_ = "select %s, %s, %s from %s"
db_tag_delete = "delete from %s where %s='%%s'"
db_tag_select = "select %s, %s from %s where %s='%%s'"
db_tag_update = "update %s set %s='%%s' where %s='%%s'"
db_tag_insert = "insert into %s (%s, %s, %s) values ('%%s', '%%s', '%%s')"
#==============================================================================
db_sql_cancel = db_tag_cancel % (db_table_name)
db_sql_create = db_tag_create % (db_table_name, db_field_name, db_f_len_name, db_field_desc, db_f_len_desc, db_field_flag)
db_sql__list_ = db_tag__list_ % (db_field_name, db_field_desc, db_field_flag, db_table_name)
db_sql_delete = db_tag_delete % (db_table_name, db_field_name)
db_sql_select = db_tag_select % (db_field_flag, db_field_desc, db_table_name, db_field_name)
db_sql_update = db_tag_update % (db_table_name, db_field_flag, db_field_name)
db_sql_insert = db_tag_insert % (db_table_name, db_field_name, db_field_desc, db_field_flag)
###############################################################################
email_notify_ = True
email__smtp__ =  'smtp.gmail.com:587'
email__from__ =  'pes0zap@payroll.it'
email___to___ = ['pes0zap@payroll.it']
email___cc___ = []
email___ccn__ = []
email_attachs = []
emailfontsize = '2' # (1|2|3|0=None)
email_subject = "ZPINFOB: Notifica ricerca Errori elaborazione ETL: %s"
email_message = """
========================================
   Messaggio automatico da SwitchOnOff
   Non rispondere a questo indirizzo!
========================================
_______________
| SQL EXECUTE |
|______________________________________________________________________________________________________________________

%s
___________________
| SEMAPHIRE STATE |
|______________________________________________________________________________________________________________________

%s

--

( Information Technology )
P&S Srl - Payroll Services
"""
###############################################################################
emailAuthUser = 'sysop@payroll.it'
emailAuthPswd = 's3rv1c3s'
###############################################################################