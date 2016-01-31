# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys
import csv
import time
import json
import pickle
import traceback
import webbrowser

from lib_external                     import gspread
from lib_external.oauth2client.client import SignedJwtAssertionCredentials, OAuth2WebServerFlow, AccessTokenRefreshError
from lib_zappyk._os_file              import _pathJoin, _fileExist

from GoogleSheets.cfg.load_cfg  import parser_args, parser_conf, logger_conf
from GoogleSheets.cfg.load_ini  import *
from GoogleSheets.src.constants import *

args = parser_args().args
conf = parser_conf().conf
logs = logger_conf().logs

gspread_scope      = GSPREAD_SCOPE

savejson           = conf.get("Base"       , "savejson"          , fallback=savejson)
username           = conf.get("Login"      , "username"          , fallback=username)
password           = conf.get("Login"      , "password"          , fallback=password)
p_encode           = conf.get("Login"      , "p_encode"          , fallback=p_encode)
servicej           = conf.get("Login"      , "servicej"          , fallback=servicej)
accountj           = conf.get("Login"      , "accountj"          , fallback=accountj)
tknstore           = conf.get("Login"      , "tknstore"          , fallback=tknstore)
filename           = conf.get("Spreadsheet", "filename"          , fallback=filename)
file_key           = conf.get("Spreadsheet", "file_key"          , fallback=file_key)
file_url           = conf.get("Spreadsheet", "file_url"          , fallback=file_url)
wks_name           = conf.get("Worksheet"  , "wks_name"          , fallback=wks_name)
csv_filename       = conf.get("InputOutput", "csv_filename"      , fallback=csv_filename)
csv_delimiter      = conf.get("InputOutput", "csv_delimiter"     , fallback=csv_delimiter)
csv_quotechar      = conf.get("InputOutput", "csv_quotechar"     , fallback=csv_quotechar)
csv_quoting        = conf.get("InputOutput", "csv_quoting"       , fallback=csv_quoting)
csv_lineterminator = conf.get("InputOutput", "csv_lineterminator", fallback=csv_lineterminator)

csv_filename       = args.csv_filename       if args.csv_filename       is not None else csv_filename
csv_delimiter      = args.csv_delimiter      if args.csv_delimiter      is not None else csv_delimiter
csv_quotechar      = args.csv_quotechar      if args.csv_quotechar      is not None else csv_quotechar
csv_lineterminator = args.csv_lineterminator if args.csv_lineterminator is not None else csv_lineterminator

filename           = args.sht_filename       if args.sht_filename       is not None else filename
file_key           = args.sht_file_key       if args.sht_file_key       is not None else file_key
file_url           = args.sht_file_url       if args.sht_file_url       is not None else file_url
wks_name           = args.wks_name           if args.wks_name           is not None else wks_name
wks_rows_resize    = args.wks_rows_resize    if args.wks_rows_resize    is not None else False
wks_cell_update    = args.wks_cell_update    if args.wks_cell_update    is not None else False
wks_rows_resize    = False                   if wks_cell_update                     else wks_rows_resize

action_write_wait  = args.action_write_wait  if args.action_write_wait  is not None else False
second_write_wait  = args.second_write_wait  if args.second_write_wait  is not None else None

wks_read   = True if args.action == 'r' else False
wks_write  = True if args.action == 'w' else False
wks_update = True if args.action == 'u' else False

servicej = _pathJoin([savejson, servicej]) if servicej is not None else servicej
accountj = _pathJoin([savejson, accountj]) if accountj is not None else accountj
tknstore = _pathJoin([savejson, tknstore]) if tknstore is not None else tknstore

login_credential_servicej = False if servicej is None else True
login_credential_accountj = False if accountj is None else not(login_credential_servicej)
login_credential          = True  if (servicej or accountj) else False

#csv_delimiter     = ','               if csv_delimiter      is None else csv_delimiter
#csv_quotechar     = '"'               if csv_quotechar      is None else csv_quotechar
#csv_quoting       = csv.QUOTE_MINIMAL if csv_quoting        is None else csv_quoting
csv_quoting        = csv.QUOTE_NONE    if csv_quoting        is None else csv_quoting
#csv_lineterminator= "\r\n"            if csv_lineterminator is None else csv_lineterminator

if second_write_wait is not None:
    (SLEEP_MULTIPLE_LINE
    ,AFTER_MULTIPLE_LINE)= second_write_wait.split('.')

if args.debug >= 1:
    logs.info('servicej                   = %s' % repr(servicej))
    logs.info('accountj                   = %s' % repr(accountj))
    logs.info('login_credentials_servicej = %s' % repr(login_credential_servicej))
    logs.info('login_credentials_accountj = %s' % repr(login_credential_accountj))
    logs.info('login_credentials          = %s' % repr(login_credential))
    logs.info('----------------------------')

###############################################################################
def main():
    init_check()

    try:
        if wks_update:

            load_file()

        else:
            glc = exec_login()

            wks = exec_spreadsheet(glc)

            if wks is not None:

                if wks_read:
                    wks_values = wks.get_all_values()
                    exec_csv_write(wks_values)

                if wks_write:
                    csv_values = exec_csv_read()
                    exec_wks_insert(wks, csv_values)

    except:
        logs.warning("(*** USCITA ANOMALA ***) o_O")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logs.traceback(exc_traceback)
        if args.debug >= 0:
            logs.warning(exc_value)
            logs.warning(LINE_SEPARATOR)
            traceback.print_exc()
            logs.warning(LINE_SEPARATOR)
            logs.error("LastError: %s" % exc_value)
        else:
            logs.error(exc_value)
        sys.exit(1)

    sys.exit(0)

###############################################################################
def init_check():
    if args.verbose:
        logs.info(LINE_SEPARATOR)
    #--------------------------------------------------------------------------

    if login_credential_servicej:
        if not _fileExist(servicej):
            logs.error('File %s not exist!' % servicej)
    if login_credential_accountj:
        if not _fileExist(accountj):
            logs.error('File %s not exist!' % accountj)

###############################################################################
def make_credential():
    credential = None
    if login_credential_servicej and servicej is not None:
        if args.verbose:
            logs.info('Create credential by json file... (%s)' % servicej)
        json_keys = json.load(open(servicej))
        json_keys_account = json_keys['client_email']
        json_keys_private = json_keys['private_key']
        credential = SignedJwtAssertionCredentials(json_keys_account, json_keys_private.encode(p_encode), gspread_scope)
        if args.verbose:
            logs.info('Create credential by json file ok (client_email=%s)' % json_keys_account)

    if login_credential_accountj and accountj is not None:
        try:
            with open(tknstore, 'rb') as file:
                credential = pickle.load(file)
            logs.info('The credential file was read, through authorize access login...')
        except:
            logs.info("The credential file can't be read, try the authenticate flow...")

        if args.verbose:
            logs.info(LINE_SEPARATOR)

        if credential is None:
            if args.verbose:
                logs.info('Create credential by json file... (%s)' % accountj)
            json_keys = json.load(open(accountj))
            json_keys_account  = json_keys['installed']['client_id']
            json_keys_private  = json_keys['installed']['client_secret']
            json_keys_redirect = json_keys['installed']['redirect_uris'][0]
            credential_flow = OAuth2WebServerFlow(json_keys_account, json_keys_private.encode(p_encode), gspread_scope, redirect_uri=json_keys_redirect)
            credential_auth_uri = credential_flow.step1_get_authorize_url()

            logs.info(LINE_PARTITION)
            step1_question_rows = ['Go to the following link in your browser:', '%s']
            step1_question_text = make_question(step1_question_rows)
            print(step1_question_text % credential_auth_uri)
            #
            #webbrowser.open_new_tab(credentials_auth_uri)
            #
            step2_question_rows = ['Enter verification code: ']
            step2_question_text = make_question(step2_question_rows)
            credentials_code = input(step2_question_text).strip()
            logs.info(LINE_PARTITION)

            credential = credential_flow.step2_exchange(credentials_code)

            if args.verbose:
                logs.info('Create credential by json file ok (client_id=%s)' % json_keys_account)

            try:
                with open(tknstore, 'wb') as file:
                    pickle.dump(credential, file, pickle.HIGHEST_PROTOCOL)
                logs.info('The credential file was save :-)')
            except:
                logs.info("The credential file can't be saved :-(")

    if credential is None:
        logs.warning(LINE_SEPARATOR)
        logs.warning('Something on Credential did not work! :-/')
    else:
        if args.verbose:
            logs.info(LINE_SEPARATOR)
    #--------------------------------------------------------------------------

    return(credential)

###############################################################################
def load_file():
    print('...DEVELOP FOR UPLOAD FILE CSV...')
    print('=================================')

    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive

    credential = make_credential()
    gauth = GoogleAuth()
    gauth.credentials = credential
#   gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    file1 = drive.CreateFile({'title': 'Hello.txt'})
    file1.SetContentString('Hello')
    file1.Upload() # Files.insert()

    file2 = drive.CreateFile()
    file2.SetContentFile(csv_filename)
    file2.Upload()
    print('Created file %s with mimeType %s' % (file2['title'], file2['mimeType']))
    # Created file hello.png with mimeType image/png

    print('=================================')
    print('...DEVELOP FOR UPLOAD FILE CSV...')

###############################################################################
def exec_login():
    gc = None
    if login_credential:

        credential = make_credential()

        if credential is not None:
            if args.verbose:
                logs.info('Login Google...')
            try:
                # Login with your Google account
                gc = gspread.authorize(credential)
            except AccessTokenRefreshError as atre:
                logs.warning(atre)
                logs.warning("Try again by clearing the credentials file! :-|")
                pass
            if args.verbose:
                logs.info('Login Google ok (by json credential)')
    else:
        if username is not None and password is not None:
            if args.verbose:
                logs.info('Login Google...')
            # Login with your Google account
            gc = gspread.login(username, password)
            if args.verbose:
                logs.info('Login Google ok (by username %s)' % username)

    if gc is None:
        logs.warning(LINE_SEPARATOR)
        logs.warning('Something on Login did not work! :-/')
    else:
        if args.verbose:
            logs.info(LINE_SEPARATOR)
    #--------------------------------------------------------------------------

    return(gc)

###############################################################################
def exec_spreadsheet(glc):
    sht = None
    wks = None
    if glc is not None:
        if sht is None and filename is not None:
            try:
                if args.verbose:
                    logs.info('Try open Spreadsheet by Name... (%s)' % filename)
                # You can open a spreadsheet by its title as it appears in Google Docs
                sht = glc.open(filename)
                if args.verbose:
                    logs.info('Try open Spreadsheet by Name ok :-)')
                else:
                    logs.info('Open Spreadsheet name: %s' % filename)
            except gspread.SpreadsheetNotFound as snf:
                logs.info("Try open Spreadsheet by Name not found!")

        if sht is None and file_key is not None:
            try:
                if args.verbose:
                    logs.info('Try open Spreadsheet by Key... (%s)' % file_key)
                # If you want to be specific, use a key (which can be extracted from the spreadsheet's url)
                sht = glc.open_by_key(file_key)
                if args.verbose:
                    logs.info('Try open Spreadsheet by Key ok :-)')
                else:
                    logs.info('Open Spreadsheet key: %s' % file_key)
            except gspread.SpreadsheetNotFound as snf:
                logs.info("Try open Spreadsheet by Key not found!")

        if sht is None and file_url is not None:
            try:
                if args.verbose:
                    logs.info('Try open Spreadsheet by Url... (%s)' % file_url)
                # Or, if you feel really lazy to extract that key, paste the entire url
                sht = glc.open_by_url(file_url)
                if args.verbose:
                    logs.info('Try open Spreadsheet by Url ok :-)')
                else:
                    logs.info('Open Spreadsheet url: %s' % file_url)
            except gspread.SpreadsheetNotFound as snf:
                logs.info("Try open Spreadsheet by Url not found!")

        if sht is None or args.debug >= 2:
            try:
                if args.verbose:
                    logs.info('Try open all Spreadsheet...')
                # Or, if you feel really lazy to extract that key, paste the entire url
                sht_all = glc.openall()
                if args.verbose:
                    logs.info('Try open all Spreadsheet ok :-)')
                    logs.info('Try find the Spreadsheet =')
                    for sht_all_obj in sht_all:
                        logs.info(' => [%s]' % sht_all_obj.title)
            except gspread.SpreadsheetNotFound as snf:
                logs.info("Try open all Spreadsheet not found anything!")

        if sht is None:
            logs.warning(LINE_SEPARATOR)
            logs.warning('Something open Spreadsheet did not work! :-(')
        else:
            if args.verbose:
                logs.info(LINE_SEPARATOR)
        #----------------------------------------------------------------------

        if sht is not None:
            str_name = str(wks_name)
            if wks_read:
                if args.verbose:
                    logs.info('Try read Worksheet... (%s)' % str_name)
                if type(wks_name) is int:
                    wks = sht.get_worksheet(wks_name)
                else:
                    wks = sht.worksheet(str_name)
                if args.verbose:
                    logs.info('Try read Worksheet ok :-)')
                else:
                    logs.info('Read Worksheet name: %s' % str_name)
            if wks_write:
                if args.verbose:
                    logs.info('Try write Worksheet... (name "%s")' % str_name)
                try:
                    if args.debug >= 2:
                        logs.info('...try get', '')
                    wks = sht.worksheet(str_name)
                    if not wks_cell_update:
                        if args.debug >= 2:
                            logs.info('...try del', '')
                        sht.del_worksheet(wks)
                except:
                    if not wks_cell_update:
                        if args.debug >= 2:
                            logs.info(' => ', '')
                    pass
                finally:
                    if not wks_cell_update:
                        if args.debug >= 2:
                            logs.info('...try add', '')
                        wks = sht.add_worksheet(title=str_name, rows=1, cols=1)
                    if args.debug >= 2:
                        logs.info('...ok!')
                if args.verbose:
                    logs.info('Try write Worksheet ok :-)')
                else:
                    logs.info('Write Worksheet name: %s' % str_name)

        if wks is None:
            logs.warning(LINE_SEPARATOR)
            logs.warning('Something read/write Worksheet did not work! :-(')
        else:
            if args.verbose:
                logs.info(LINE_SEPARATOR)
        #----------------------------------------------------------------------

    return(wks)

###############################################################################
def exec_csv_write(wks_values):
    if args.debug >= 1:
        logs.info('wks values=')
        for values in wks_values:
            logs.info(values)

    fileout = None
    std_out = False
    if csv_filename == CHAR_STD_INOUT:
        fileout = sys.stdout
        std_out = True
        logs.info('Write csv rows on STDOUT:')
    else:
        try:
            fileout = open(csv_filename, 'w')
            logs.info('Write to file csv: %s' % csv_filename)
        except:
            fileout = sys.stdout
            std_out = True
            logs.info('File csv not set, write on STDOUT:')

    if std_out:
        logs.info(LINE_PARTITION)
    #csv_values= csv.writer(fileout)
    csv_values = csv.writer(fileout, delimiter=csv_delimiter, quotechar=csv_quotechar, quoting=csv_quoting, lineterminator=csv_lineterminator)
    csv_values.writerows(wks_values)
    if std_out:
        logs.info(LINE_PARTITION)

###############################################################################
def exec_csv_read():
    filein = None
    std_in = False
    if csv_filename == CHAR_STD_INOUT:
        filein = sys.stdin
        std_in = True
        logs.info('Read csv rows on STDIN:')
    else:
        try:
            filein = open(csv_filename, 'r')
            logs.info('Read on file csv: %s' % csv_filename)
        except:
            filein = sys.stdin
            std_in = True
            logs.info('File csv not set, read on STDIN:')

    if std_in:
        logs.info(LINE_PARTITION)
    #csv_values= list(csv.reader(filein)
    #csv_values= list(csv.reader(filein, delimiter=csv_delimiter, quotechar=csv_quotechar, quoting=csv_quoting, lineterminator=csv_lineterminator))
    csv_values = list(csv.reader(filein, delimiter=csv_delimiter))
    if std_in:
        logs.info(LINE_PARTITION)

    if args.debug >= 1:
        logs.info('csv values=')
        for values in csv_values:
            logs.info(values)

    return(csv_values)

###############################################################################
def exec_wks_insert(wks, csv_values):
    if wks is not None:
        #--------------------------------------------------------------
        #if args.wks_resize:
        #    rows = len(csv_values)
        #    cols = 0
        #    for line_values in csv_values:
        #        cols = len(line_values)
        #        break
        #    wks.resize(rows, cols)
        #--------------------------------------------------------------
        row = 0
        col = 0
        rof = len(csv_values)
        rln = len(str(rof))
        log = 'Insert %' + str(rln) + 's/%s'
        if args.debug >= 1:
            log = log + ' %s'
        else:
            log = log + 'row on spreadsheet...'
        for row_values in csv_values:
            if row == 0:
                col = len(row_values)
            row += 1
            if args.debug >= 1:
                logs.info(log % (row, rof, row_values))
            else:
                logs.info(log % (row, rof))

            if wks_cell_update:
                x = row
                y = 0
                for cell in row_values:
                    y += 1
                    wks.update_cell(x, y, cell)
            else:
                wks.insert_row(row_values, row)

            if action_write_wait:
                if (row % AFTER_MULTIPLE_LINE) == 0:
                    logs.info('...sleep %s seconds...' % SLEEP_MULTIPLE_LINE)
                    wait(SLEEP_MULTIPLE_LINE)

        logs.info('Insert done!')
        if wks_rows_resize:
            wks.resize(row, col)

###############################################################################
def make_question(rows):
    line = rows[0]
    rive = '_' * len(line)
    rows.insert(0, rive)
    text = "\n".join(rows)
    return(text)

###############################################################################
def wait(seconds):
    import time
    time.sleep(seconds)

###############################################################################
def open_file(file):
#CZ#return(open(file))
#CZ#return(open(file, 'r', encoding="ascii"     , errors="surrogateescape"))
#CZ#return(open(file, 'r', encoding="ascii"     , errors="replace"))
#CZ#return(open(file, 'r', encoding="utf-8"     , errors="replace"))
    return(open(file, 'r', encoding="iso-8859-1", errors="replace"))
