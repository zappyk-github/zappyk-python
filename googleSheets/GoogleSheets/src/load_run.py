# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os
import sys
import csv
import json
import pickle
import traceback
import webbrowser

from lib_external                     import gspread
from lib_external.oauth2client.client import SignedJwtAssertionCredentials
from lib_external.oauth2client.client import OAuth2WebServerFlow

from GoogleSheets.cfg.load_cfg  import parser_args, parser_conf, logger_conf
from GoogleSheets.cfg.load_ini  import *
from GoogleSheets.src.constants import *

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

servicej = os.path.sep.join([savejson, servicej]) if servicej is not None else servicej
accountj = os.path.sep.join([savejson, accountj]) if accountj is not None else accountj
tknstore = os.path.sep.join([savejson, tknstore]) if tknstore is not None else tknstore

login_credential_servicej = False if servicej is None else True
login_credential_accountj = False if accountj is None else not(login_credential_servicej)
login_credential          = True  if (servicej or accountj) else False

csv_delimiter      = ';'               if csv_delimiter      is None else csv_delimiter
csv_quotechar      = '"'               if csv_quotechar      is None else csv_quotechar
csv_quoting        = csv.QUOTE_MINIMAL if csv_quoting        is None else csv_quoting
csv_lineterminator = '\n'              if csv_lineterminator is None else csv_lineterminator

if args.debug >= 1:
    logs.info('servicej                   = %s' % servicej)
    logs.info('accountj                   = %s' % accountj)
    logs.info('login_credentials_servicej = %s' % login_credential_servicej)
    logs.info('login_credentials_accountj = %s' % login_credential_accountj)
    logs.info('login_credentials          = %s' % login_credential)

###############################################################################
def main():
    if login_credential_servicej:
        if not os.path.isfile(servicej):
            logs.error('File %s not exist!' % servicej)
    if login_credential_accountj:
        if not os.path.isfile(accountj):
            logs.error('File %s not exist!' % accountj)

    try:
        if args.verbose:
            logs.info(LINE_SEPARATOR)
        #######################################################################

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
                # Login with your Google account
                gc = gspread.authorize(credential)
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
            logs.warning('Something on Login did not work! :-(')
        else:
            if args.verbose:
                logs.info(LINE_SEPARATOR)
        #######################################################################

        sht = None
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
        #######################################################################

        wks = None
        if sht is not None:
            if args.verbose:
                logs.info('Try read Worksheet... (%s)' % wks_name)
            wks = sht.get_worksheet(wks_name)
            if args.verbose:
                logs.info('Try read Worksheet ok :-)')

        if wks is None:
            logs.warning(LINE_SEPARATOR)
            logs.warning('Something read Worksheet did not work! :-(')
        else:
            if args.verbose:
                logs.info(LINE_SEPARATOR)
        #######################################################################

        if wks is not None:
            wks_values = wks.get_all_values()

            if args.debug >= 1:
                logs.info('wks_values=\n[%s]' % wks_values)

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
            #file_csv_writer = csv.writer(fileout)
            #file_csv_writer = csv.writer(fileout, delimiter=csv_delimiter, quotechar=csv_quotechar, quoting=csv_quoting, lineterminator=csv_lineterminator)
            #file_csv_writer = csv.writer(fileout, delimiter=csv_delimiter, quotechar=csv_quotechar, lineterminator=csv_lineterminator)
            #file_csv_writer = csv.writer(fileout, delimiter=csv_delimiter, lineterminator=csv_lineterminator)
            file_csv_writer = csv.writer(fileout, delimiter=csv_delimiter)
            file_csv_writer.writerows(wks_values)
            if std_out:
                logs.info(LINE_PARTITION)

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
def open_file(file):
#CZ#return(open(file))
#CZ#return(open(file, 'r', encoding="ascii"     , errors="surrogateescape"))
#CZ#return(open(file, 'r', encoding="ascii"     , errors="replace"))
#CZ#return(open(file, 'r', encoding="utf-8"     , errors="replace"))
    return(open(file, 'r', encoding="iso-8859-1", errors="replace"))

###############################################################################
def make_question(rows):
    line = rows[0]
    rive = '_' * len(line)
    rows.insert(0, rive)
    text = "\n".join(rows)
    return(text)