# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys
import csv
import json
import pickle
import traceback
import webbrowser

from lib_external                     import gspread
from lib_external.oauth2client.client import SignedJwtAssertionCredentials, OAuth2WebServerFlow, AccessTokenRefreshError
from lib_zappyk._os_file              import _pathJoin, _fileExist

from googleSheets.GoogleSheets.cfg.load_cfg  import parser_args, parser_conf, logger_conf
from googleSheets.GoogleSheets.cfg.load_ini  import *
from googleSheets.GoogleSheets.src.constants import *

args = parser_args().args
conf = parser_conf().conf
logs = logger_conf().logs

savejson           = conf.get("Base"       , "savejson"          , fallback=savejson)
username           = conf.get("Login"      , "username"          , fallback=username)
password           = conf.get("Login"      , "password"          , fallback=password)
p_encode           = conf.get("Login"      , "p_encode"          , fallback=p_encode)
servicej           = conf.get("Login"      , "servicej"          , fallback=servicej)
accountj           = conf.get("Login"      , "accountj"          , fallback=accountj)
urlscope           = conf.get("Login"      , "urlscope"          , fallback=urlscope)
tknstore           = conf.get("Login"      , "tknstore"          , fallback=tknstore)
openname           = conf.get("Spreadsheet", "openname"          , fallback=openname)
open_key           = conf.get("Spreadsheet", "open_key"          , fallback=open_key)
open_url           = conf.get("Spreadsheet", "open_url"          , fallback=open_url)
wks_name           = conf.get("Worksheet"  , "wks_name"          , fallback=wks_name)
csv_file_name      = conf.get("InputOutput", "csv_file_name"     , fallback=csv_file_name)
csv_delimiter      = conf.get("InputOutput", "csv_delimiter"     , fallback=csv_delimiter)
csv_quotechar      = conf.get("InputOutput", "csv_quotechar"     , fallback=csv_quotechar)
csv_quoting        = conf.get("InputOutput", "csv_quoting"       , fallback=csv_quoting)
csv_lineterminator = conf.get("InputOutput", "csv_lineterminator", fallback=csv_lineterminator)

wks_read  = True if args.action == 'r' else False
wks_write = True if args.action == 'w' else False

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

if args.debug >= 1:
    logs.info('servicej                   = %s' % servicej)
    logs.info('accountj                   = %s' % accountj)
    logs.info('login_credentials_servicej = %s' % login_credential_servicej)
    logs.info('login_credentials_accountj = %s' % login_credential_accountj)
    logs.info('login_credentials          = %s' % login_credential)

###############################################################################
def main():
    init_check()

    try:
        gc = exec_login()

        wks = exec_spreadsheet(gc)

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
    if login_credential_servicej:
        if not _fileExist(servicej):
            logs.error('File %s not exist!' % servicej)
    if login_credential_accountj:
        if not _fileExist(accountj):
            logs.error('File %s not exist!' % accountj)

###############################################################################
def exec_login():
    if args.verbose:
        logs.info(LINE_SEPARATOR)
    #--------------------------------------------------------------------------

    gc = None
    if login_credential:

        credential = None
        if login_credential_servicej and servicej is not None:
            if args.verbose:
                logs.info('Create credential by json file... (%s)' % servicej)
            json_keys = json.load(open(servicej))
            json_keys_account = json_keys['client_email']
            json_keys_private = json_keys['private_key']
            credential = SignedJwtAssertionCredentials(json_keys_account, json_keys_private.encode(p_encode), urlscope)
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
                credential_flow = OAuth2WebServerFlow(json_keys_account, json_keys_private.encode(p_encode), urlscope, redirect_uri=json_keys_redirect)
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
        if args.verbose:
            logs.warning(LINE_SEPARATOR)
        logs.warning('Something on Login did not work! :-/')
    else:
        if args.verbose:
            logs.info(LINE_SEPARATOR)
    #--------------------------------------------------------------------------

    return(gc)

###############################################################################
def exec_spreadsheet(gc):
    sht = None
    wks = None
    if gc is not None:
        if sht is None and openname is not None:
            try:
                if args.verbose:
                    logs.info('Try open Spreadsheet by Name... (%s)' % openname)
                # You can open a spreadsheet by its title as it appears in Google Docs
                sht = gc.open(openname)
                if args.verbose:
                    logs.info('Try open Spreadsheet by Name ok :-)')
            except gspread.SpreadsheetNotFound as snf:
                logs.info("Try open Spreadsheet by Name not found!")

        if sht is None and open_key is not None:
            try:
                if args.verbose:
                    logs.info('Try open Spreadsheet by Key... (%s)' % open_key)
                # If you want to be specific, use a key (which can be extracted from the spreadsheet's url)
                sht = gc.open_by_key(open_key)
                if args.verbose:
                    logs.info('Try open Spreadsheet by Key ok :-)')
            except gspread.SpreadsheetNotFound as snf:
                logs.info("Try open Spreadsheet by Key not found!")

        if sht is None and open_url is not None:
            try:
                if args.verbose:
                    logs.info('Try open Spreadsheet by Url... (%s)' % open_url)
                # Or, if you feel really lazy to extract that key, paste the entire url
                sht = gc.open_by_url(open_url)
                if args.verbose:
                    logs.info('Try open Spreadsheet by Url ok :-)')
            except gspread.SpreadsheetNotFound as snf:
                logs.info("Try open Spreadsheet by Url not found!")

        if args.debug >= 2:
            try:
                if args.verbose:
                    logs.info('Try open all Spreadsheet...')
                # Or, if you feel really lazy to extract that key, paste the entire url
                sht_all = gc.openall()
                if args.verbose:
                    logs.info('Try open all Spreadsheet ok :-)')
                    logs.info('Spreadsheet = [%s]' % sht_all)
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
            if wks_write:
                if args.verbose:
                    logs.info('Try write Worksheet... (name "%s")' % str_name)
                try:
                    if args.debug >= 2:
                        logs.info('...try get', '')
                    wks = sht.worksheet(str_name)
                    if args.debug >= 2:
                        logs.info('...try del', '')
                    sht.del_worksheet(wks)
                except:
                    if args.debug >= 2:
                        logs.info(' => ', '')
                    pass
                finally:
                    if args.debug >= 2:
                        logs.info('...try add', '')
                    wks = sht.add_worksheet(title=str_name, rows=1, cols=1)
                    if args.debug >= 2:
                        logs.info('...ok!')
                if args.verbose:
                    logs.info('Try write Worksheet ok :-)')

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
    if csv_file_name == CHAR_STD_INOUT:
        fileout = sys.stdout
        std_out = True
        logs.info('Write csv rows on STDOUT:')
    else:
        try:
            fileout = open(csv_file_name, 'w')
            logs.info('Write to file csv: %s' % csv_file_name)
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
    if csv_file_name == CHAR_STD_INOUT:
        filein = sys.stdin
        std_in = True
        logs.info('Read csv rows on STDIN:')
    else:
        try:
            filein = open(csv_file_name, 'r')
            logs.info('Read on file csv: %s' % csv_file_name)
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
        #rows = len(csv_values)
        #cols = 0
        #for line_values in csv_values:
        #    cols = len(line_values)
        #    break
        #wks.resize(rows, cols)
        #--------------------------------------------------------------
        row = 0
        col = 0
        rof = len(csv_values)
        rln = len(str(rof))
        log = 'Insert %' + str(rln) + 's/%s'
        if args.debug >= 1:
            log = log + ' %s'
        else:
            log = log + 'row on spreadsheet ...'
        for row_values in csv_values:
            if row == 0:
                col = len(row_values)
            row += 1
            if args.debug >= 1:
                logs.info(log % (row, rof, row_values))
            else:
                logs.info(log % (row, rof))
            wks.insert_row(row_values, row)
        logs.info('Insert done!')
        wks.resize(row, col)

###############################################################################
def make_question(rows):
    line = rows[0]
    rive = '_' * len(line)
    rows.insert(0, rive)
    text = "\n".join(rows)
    return(text)

###############################################################################
def open_file(file):
#CZ#return(open(file))
#CZ#return(open(file, 'r', encoding="ascii"     , errors="surrogateescape"))
#CZ#return(open(file, 'r', encoding="ascii"     , errors="replace"))
#CZ#return(open(file, 'r', encoding="utf-8"     , errors="replace"))
    return(open(file, 'r', encoding="iso-8859-1", errors="replace"))