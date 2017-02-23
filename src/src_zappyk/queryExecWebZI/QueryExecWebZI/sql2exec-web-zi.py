#!/usr/bin/env python-payroll
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os, re, sys, time, copy, argparse

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

_version = '0.1'

_project = 'QueryExecWebZI'

_description = '''
Query Executed on WEB Zucchetti Infinity Portal through page RUN-SQL.
'''

_epilog = "Version: %s" % _version

_sdtin_ = '-'

########################################################################################################################
def _getconfig(run='', config_help=False):
    config = {}
    conf_h = {}

    if config_help\
    or run == 'pes_test':
        config['username'] = 'administrator'
        config['password'] = '!S3rv1c3s!'
        config['basepath'] = 'https://test.payroll.it/HRPW'
        if config_help:
            conf_h['pes_test'] = copy.deepcopy(config)

    if config_help\
    or run == 'accademia':
        config['username'] = 'administrator'
        config['password'] = '!4cc4d3m14!'
        config['basepath'] = 'https://saas.hrzucchetti.it/hrppbs'
        if config_help:
            conf_h['accademia'] = copy.deepcopy(config)

    if config_help\
    or run == 'cassapadana':
        config['username'] = 'administrator'
        config['password'] = 'C@33@p@d@n@!2016'
        config['basepath'] = 'https://hr.cassapadana.it/ERM'
        if config_help:
            conf_h['cassapadana'] = copy.deepcopy(config)

    if config_help:
        config = conf_h

    return(config)

########################################################################################################################
class MyArgumentParser(argparse.ArgumentParser):
    def print_help(self, file=None):
        print(self.format_help())
        print('Configurations RUN available are:')
        config = _getconfig(config_help=True)
    #CZ#import pprint
    #CZ#pprint.pprint(config, indent=2, depth=2)
        for run in config:
            config[run]['password'] = config[run]['password'][:3] + '***'
            print(' · %s' % run)
            for key in config[run]:
                print('\t\t%s: %s' % (key, config[run][key]))
            print('')
        self.exit()
########################################################################################################################
def _getargs():
#CZ#parser = argparse.ArgumentParser(description=_description, epilog=_epilog, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=120)
    formatter = lambda prog: argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=50, width=120)
#CZ#formatter = lambda prog: argparse.RawDescriptionHelpFormatter(prog, max_help_position=50, width=120)
#CZ#parser = argparse.ArgumentParser(description=_description, epilog=_epilog, formatter_class=formatter) #, argument_default=not argparse.SUPPRESS)
    parser = MyArgumentParser(description=_description, epilog=_epilog, formatter_class=formatter) #, argument_default=not argparse.SUPPRESS)

#CZ#pgroup.add_argument('-p' , '--power'       , help='display a power of a given number'    , type=int           , choices=[1,2,3,4,5])
#CZ#pgroup.add_argument('-s' , '--square'      , help='display a square of a given number'   , type=int)
    parser.add_argument('-d' , '--debug'       , help='increase output debug'                , action='count'     , default=0)
    parser.add_argument('-v' , '--verbose'     , help='output verbosity'                     , action='store_true')
    parser.add_argument('-V' , '--version'     , help='print version number'                 , action='version'   , version='%(prog)s '+_version)
    parser.add_argument('-r' , '--run'         , help='run execute, read below for more info', type=str           , required=True)
    parser.add_argument('-s' , '--sql'         , help=('sql execute, %s for STDIN' % _sdtin_), type=str           , required=True)
#CZ#parser.add_argument('name'                 , help='Name')
#CZ#parser.add_argument('surname'              , help='Surnamename')

    args = parser.parse_args()

    return(args)

########################################################################################################################

args = _getargs()

debug_step = args.debug
verbose_on = args.verbose
urlweb_RUN = args.run
urlweb_SQL = args.sql
config_RUN = _getconfig(urlweb_RUN)

if urlweb_SQL == _sdtin_:
    urlweb_SQL = [line.strip() for line in sys.stdin.readlines()]
    urlweb_SQL = '\n'.join(urlweb_SQL)

########################################################################################################################

browser_wd = 'Firefox' # = 'Chrome' # = 'PhantomJS'

########################################################################################################################

set_user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

url_base_path_ = config_RUN['basepath']
url_page_home_ = url_base_path_ + "/HRPW/jsp/home.jsp"
url_page_login = url_base_path_ + "/jsp/login.jsp"
url_page_query = url_base_path_ + "/servlet/cost_bexecrunsql?m_cWindowName=main"

type_username_ = config_RUN['username']
type_password_ = config_RUN['password']
find_username_ = 'm_cUserName'
find_password_ = 'm_cPassword'

name_titleHome = 'Infinity Zucchetti'
find_typeLogin = "//*[@type='submit']"   #    => find_element_by_xpath(find_typeLogin)
find_execQuery = ".*_RunButton"          # id => find_element_by_xpath("//*[@id='.*_RunButton']")
find_execResul = ".*_FrameResult_iframe" # id => find_element_by_xpath("//*[@id='.*_FrameResult_iframe']")
find_theLogout = ".*_imgLogouthref"      # id => find_element_by_xpath("//*[@id='.*_imgLogouthref']"")

find_queryArea = 'MMSQL'
find_queryExec = urlweb_SQL

screenshot_tag = 'screenshot-%s.png'
linebuffer_log = []

h2s_field_char = '|'
csv_field_char = '|'

write_valsNULL = ''
write_colsSkip = '---'
write_lineSkip = True

wait_on_step_1 = 3
wait_on_step_2 = 5
wait_on_step_3 = 5

########################################################################################################################

browser_wd_PhantomJS_screenshot = screenshot_tag
browser_wd_PhantomJS_htmlstring = '<html><body><div style="background-color:red;height:500px;width:500px;">This is a png</div></body></html>'
browser_wd_PhantomJS_overralert = 'window.alert=function(message){return true;}'
browser_wd_PhantomJS_overrconfi = 'window.confirm=function(message){return true;}'
browser_wd_PhantomJS_override_f = 'cost_bexecrunsql.CtxLoad_=function(){return true;}'

########################################################################################################################
VirDisplay  = True
InitBrowser = True
PageLogin   = True
PageTitle   = True
PageQuery   = True
PageAlert   = True
InsQuery    = True
ExcQuery    = InsQuery
ResQuery    = ExcQuery
PageBack    = False
PageLogout  = False
DoneBrowser = True
WriteBuffer = True
PrintBuffer = False
ExitCode    = 0
########################################################################################################################

if debug_step >= 1:
    PrintBuffer = True

if debug_step >= 2:
    WriteBuffer = False

########################################################################################################################
def _write(string=''):
    lineend = ''
    if WriteBuffer:
        if PrintBuffer:
            if string != '':
                if string != '.':
                #CZ#print(':', end=lineend) # valido per python >= 3
                    sys.stdout.write(':')   # valido per python >= 2
                else:
                #CZ#print('.', end=lineend) # valido per python >= 3
                    sys.stdout.write('.')   # valido per python >= 2
        linebuffer_log.append(string)
    else:
    #CZ#print(string, end=lineend) # valido per python >= 3
        sys.stdout.write(string)   # valido per python >= 2
    sys.stdout.flush()

########################################################################################################################
def _writeln(string=''):
    lineend = '\n'
    if WriteBuffer:
        if PrintBuffer:
            if string != '':
            #CZ#print(':')
                print(':%s' % string)
            else:
                print('')
        linebuffer_log.append(string + lineend)
    else:
        print(string)

########################################################################################################################
def _writebuffer():
    if WriteBuffer:
        print(_repeat_string('#', 80))
        print(''.join(linebuffer_log))
        print(_repeat_string('#', 80))

########################################################################################################################
def _writesql(browser_page_source=''):
    ps = browser_page_source
#CZ#if isinstance(ps, unicode):
#CZ#    ps = ps.encode('utf-8')

    if verbose_on:
        print("ps=[[%s]]" % ps)
        print("ps={{%s}}" % type(ps))
    tt = _html_table2text(ps)

    if verbose_on:
            print("tt=[[%s]]" % tt)
            print("tt={{%s}}" % type(tt))
    lc = _writecsv(tt)

    if verbose_on:
        print("lc=[[%s]]" % lc)
        print("lc={{%s}}" % type(lc))

    ws = '\n'.join(lc)

    if verbose_on:
        print("ws=((%s))" % ws)

    return(ws)

########################################################################################################################
def _writecsv(data='', h2s_sep_field=h2s_field_char, csv_field_char=csv_field_char, trim_field=True):
#CZ#if not isinstance(data, str):   # valido per python >= 3
#CZ#    data = data.encode('utf-8') # valido per python >= 3
    if isinstance(data, unicode):   # valido per python  = 2
        data = data.encode('utf-8') # valido per python  = 2

    text_in = []
#CZ#if type(data) is bytes: # valido per python >= 3
    if type(data) is str:   # valido per python  = 2
        text_in = data.split('\n')
    else:
        text_in = data

#CZ#print("ti=[[%s]]" % text_in)
#CZ#print("ti={{%s}}" % type(text_in))

    cols_max = {}

    line_tmp = []
    for line in text_in:
        if line.strip() == '':
            continue

        this_row = line.split(h2s_sep_field)
        if trim_field:
        #CZ#this_row = map(str.strip, this_row)           # valido per python >= 3
            this_row = map(lambda s: s.strip(), this_row) # valido per python >= 2

    #CZ#colsSkip = write_colsSkip
        lineSkip = write_lineSkip
        this_tmp = []
        for i, v in enumerate(this_row):
            l = len(v)
            m = cols_max[i] if i in cols_max.keys() else 0
        #CZ#if v != colsSkip:
            if v != write_colsSkip:
                lineSkip = False
                if l > m:
                    cols_max[i] = l
            if v.upper() == 'NULL':
                v = write_valsNULL
            this_tmp.append(v)
        if not lineSkip:
            line_tmp.append(this_tmp)

    rows_tmp = []
    for rows in line_tmp:
        this_tmp = []
        for i, v in enumerate(rows):
            fieldmax = cols_max[i]
            this_tmp.append(v.ljust(fieldmax))
        rows_tmp.append(this_tmp)

    rows_out = []
    for r in rows_tmp:
    #CZ#l = sep_field.join(r)
        l = '%s%s%s' % (csv_field_char, csv_field_char.join(r), csv_field_char)
        rows_out.append(l)

#CZ#text_out = '\n'.join(rows_out)
    text_out = rows_out

    return(text_out)

########################################################################################################################
def _repeat_string(string='', repetitions=0):
    return(''.join([ string for n in range(repetitions)]))

########################################################################################################################
def _sleep(count=1, view=1):
    if view == 2:
        _write('sleep(%s' % count)
    for i in range(0, count, 1):
        time.sleep(1)
        if view == 2:
            _write(count -i -1)
        if view == 1:
            _write('.')
    if view == 2:
        _write(')')

########################################################################################################################
def _read(string=''):
    import fileinput
    _write(string)
    for input_line in fileinput.input():
        pass
    return(input_line)

########################################################################################################################
def _read_file(file=''):
#CZ#text = None
#CZ#with open(file, 'r') as f:
#CZ#    text = f.readlines()
    text = open(file).read()
    return(text)

########################################################################################################################
def _html_table2text(html_table='', body_width=300):
    import html2text
#CZ#text = html2text.html2text(html_table, bodywidth=body_width).encode('utf-8')
    text = html2text.html2text(html_table, bodywidth=body_width)
    return(text)

########################################################################################################################
def find_element_by_regex(bw=None, xpath='id', regex=None, debug=0):
    xpa = []
    xps = bw.find_elements_by_xpath('//*[@%s]' % xpath)
    for xp in xps:
        ga = xp.get_attribute(xpath)
        if debug == 2:
            _write('find [%s]=[%s] => ' % (xpath, ga))
        if re.search(regex, ga):
            xpa.append(ga)
            if debug == 2:
                _writeln('Ok')
            if debug == 1:
                _writeln('find [%s]=[%s]' % (xpath, ga))
        else:
            if debug == 2:
                _writeln()
    return(xpa)

########################################################################################################################
def _browser_is_Firefox(browser_webdrive):
    if browser_webdrive == 'Firefox':
        return(True)
    return(False)
########################################################################################################################
def _browser_is_PhantomJS(browser_webdrive):
    if browser_webdrive == 'PhantomJS':
        return(True)
    return(False)
########################################################################################################################
def _browser_is_Chrome(browser_webdrive):
    if browser_webdrive == 'Chrome':
        return(True)
    return(False)
########################################################################################################################
def _browser(browser_webdrive):
    browser = None
    #___________________________________________________________________________________________________________________
    if _browser_is_Firefox(browser_webdrive):
    #CZ#dcap = dict(DesiredCapabilities.FIREFOX)
    #CZ#dcap['log_path'] = os.devnull
        browser = webdriver.Firefox()
    #CZ#browser = webdriver.Firefox(firefox_profile=webdriver.FirefoxProfile())
    #___________________________________________________________________________________________________________________
    if _browser_is_PhantomJS(browser_webdrive):
    #   dcap = dict(DesiredCapabilities.PHANTOMJS)
    #   print(dcap)
    #   dcap['handlesAlerts'] = True
    #   print(dcap)
        browser = webdriver.PhantomJS()
    #CZ#browser = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
        browser.set_window_size(1920, 1080)
        browser.implicitly_wait(wait_on_step_3)
    #   browser.get_screenshot_as_file(browser_wd_PhantomJS_screenshot % 0)
    #___________________________________________________________________________________________________________________
    if _browser_is_Chrome(browser_webdrive):
        browser = webdriver.Chrome()
    #___________________________________________________________________________________________________________________
    if browser is None:
        raise Exception('Browser %s not implemented :-(' % browser_webdrive)
    return(browser)

########################################################################################################################
########################################################################################################################

try:
########################################################################################################################
###  #     #  ###  #######        ######   ###   #####   ######   #           #     #     #
 #   ##    #   #      #           #     #   #   #     #  #     #  #          # #     #   #
 #   # #   #   #      #           #     #   #   #        #     #  #         #   #     # #
 #   #  #  #   #      #           #     #   #    #####   ######   #        #     #     #
 #   #   # #   #      #           #     #   #         #  #        #        #######     #
 #   #    ##   #      #           #     #   #   #     #  #        #        #     #     #
###  #     #  ###     #           ######   ###   #####   #        #######  #     #     #
########################################################################################################################
    if VirDisplay:
    #CZ#vdisplay = Xvfb()
    #CZ#vdisplay = Display(visible=0, size=(800, 600), use_xauth=True)
        vdisplay = Display(visible=0, size=(800, 600))
        vdisplay.start()

########################################################################################################################
###  #     #  ###  #######        ######   ######   #######  #     #   #####   #######  ######
 #   ##    #   #      #           #     #  #     #  #     #  #  #  #  #     #  #        #     #
 #   # #   #   #      #           #     #  #     #  #     #  #  #  #  #        #        #     #
 #   #  #  #   #      #           ######   ######   #     #  #  #  #   #####   #####    ######
 #   #   # #   #      #           #     #  #   #    #     #  #  #  #        #  #        #   #
 #   #    ##   #      #           #     #  #    #   #     #  #  #  #  #     #  #        #    #
###  #     #  ###     #           ######   #     #  #######   ## ##    #####   #######  #     #
########################################################################################################################
    browser = None
    if InitBrowser:
        _writeln("Open browser %s." % browser_wd)
        browser = _browser(browser_wd)
        _writeln("Open page login.")
        _write("Load page login %s:" % url_page_login)
        browser.get(url_page_login)
        _sleep(wait_on_step_2)
        _writeln()
        #_______________________________________________________________________________________________________________
        if debug_step >= 5:
            browser.save_screenshot(screenshot_tag % '1-login')
            pass

########################################################################################################################
######      #      #####   #######        #        #######   #####   ###  #     #
#     #    # #    #     #  #              #        #     #  #     #   #   ##    #
#     #   #   #   #        #              #        #     #  #         #   # #   #
######   #     #  #  ####  #####          #        #     #  #  ####   #   #  #  #
#        #######  #     #  #              #        #     #  #     #   #   #   # #
#        #     #  #     #  #              #        #     #  #     #   #   #    ##
#        #     #   #####   #######        #######  #######   #####   ###  #     #
########################################################################################################################
    if PageLogin:
        _write("Login credential:")
        username = browser.find_element_by_name(find_username_)
        password = browser.find_element_by_name(find_password_)
    #   if _browser_is_PhantomJS(browser_wd):
    #       wait = WebDriverWait(browser, wait_step3)
    #       password = wait.until(EC.presence_of_element_located((By.NAME, find_password_)))
    #       password = wait.until(EC.visibility_of_element_located((By.NAME, find_password_)))
    #       pass
        username.clear()
        username.send_keys(type_username_)
        password.clear()
        password.send_keys(type_password_)
        login_attempt = browser.find_element_by_xpath(find_typeLogin)
        login_attempt.click()
        _sleep(wait_on_step_1)
        _writeln()
        #_______________________________________________________________________________________________________________
        if _browser_is_PhantomJS(browser_wd):
        #   browser.execute_script(browser_wd_PhantomJS_overralert)
        #   browser.execute_script(browser_wd_PhantomJS_override_f)
            pass
        if debug_step >= 5:
            browser.save_screenshot(screenshot_tag % '2-home')
            pass

########################################################################################################################
######      #      #####   #######        #######  ###  #######  #        #######
#     #    # #    #     #  #                 #      #      #     #        #
#     #   #   #   #        #                 #      #      #     #        #
######   #     #  #  ####  #####             #      #      #     #        #####
#        #######  #     #  #                 #      #      #     #        #
#        #     #  #     #  #                 #      #      #     #        #
#        #     #   #####   #######           #     ###     #     #######  #######
########################################################################################################################
    if PageTitle:
        _writeln("Home page?")
        if browser.title != name_titleHome:
            raise Exception("Home page not fond!")

########################################################################################################################
######      #      #####   #######         #####   #     #  #######  ######   #     #
#     #    # #    #     #  #              #     #  #     #  #        #     #   #   #
#     #   #   #   #        #              #     #  #     #  #        #     #    # #
######   #     #  #  ####  #####          #     #  #     #  #####    ######      #
#        #######  #     #  #              #   # #  #     #  #        #   #       #
#        #     #  #     #  #              #    #   #     #  #        #    #      #
#        #     #   #####   #######         #### #   #####   #######  #     #     #
########################################################################################################################
    if PageQuery:
        _writeln("Open page query.")
        _write("Load page query %s:" % url_page_query)
        browser.get(url_page_query)
        _sleep(wait_on_step_1)
        _writeln()

########################################################################################################################
######      #      #####   #######           #     #        #######  ######   #######
#     #    # #    #     #  #                # #    #        #        #     #     #
#     #   #   #   #        #               #   #   #        #        #     #     #
######   #     #  #  ####  #####          #     #  #        #####    ######      #
#        #######  #     #  #              #######  #        #        #   #       #
#        #     #  #     #  #              #     #  #        #        #    #      #
#        #     #   #####   #######        #     #  #######  #######  #     #     #
########################################################################################################################
    if PageAlert:
        _write("Page alert accept:")
        if _browser_is_Firefox(browser_wd)\
        or _browser_is_Chrome(browser_wd):
        #CZ#browser.switch_to_alert().accept()
            browser.switch_to.alert.accept()
        if _browser_is_PhantomJS(browser_wd):
            pass
        _sleep(wait_on_step_1)
        _writeln()
        #_______________________________________________________________________________________________________________
    #CZ#_writeln("\t|\n\t| here is Insert & Execute query\n\t|")
        if debug_step >= 5:
            browser.save_screenshot(screenshot_tag % '3-query')
            pass

########################################################################################################################
###  #     #   #####   #######  ######   #######         #####   #     #  #######  ######   #     #
 #   ##    #  #     #  #        #     #     #           #     #  #     #  #        #     #   #   #
 #   # #   #  #        #        #     #     #           #     #  #     #  #        #     #    # #
 #   #  #  #   #####   #####    ######      #           #     #  #     #  #####    ######      #
 #   #   # #        #  #        #   #       #           #   # #  #     #  #        #   #       #
 #   #    ##  #     #  #        #    #      #           #    #   #     #  #        #    #      #
###  #     #   #####   #######  #     #     #            #### #   #####   #######  #     #     #
########################################################################################################################
    if InsQuery:
        _write("Insert query:")
        sql_area = browser.find_element_by_name(find_queryArea)
        sql_area.send_keys(find_queryExec)
        _sleep(wait_on_step_1)
        _writeln()
        #_______________________________________________________________________________________________________________
        if debug_step >= 5:
            browser.save_screenshot(screenshot_tag % '3-query-1-insert')
            pass

########################################################################################################################
#######  #     #  #######   #####   #     #  #######  #######         #####   #     #  #######  ######   #     #
#         #   #   #        #     #  #     #     #     #              #     #  #     #  #        #     #   #   #
#          # #    #        #        #     #     #     #              #     #  #     #  #        #     #    # #
#####       #     #####    #        #     #     #     #####          #     #  #     #  #####    ######      #
#          # #    #        #        #     #     #     #              #   # #  #     #  #        #   #       #
#         #   #   #        #     #  #     #     #     #              #    #   #     #  #        #    #      #
#######  #     #  #######   #####    #####      #     #######         #### #   #####   #######  #     #     #
########################################################################################################################
    if ExcQuery:
        _write("Execute query:")
        ids_exec = find_element_by_regex(browser, 'id', find_execQuery)
        sql_exec = browser.find_element_by_id(ids_exec[0])
        sql_exec.click()
        _sleep(wait_on_step_2)
        _writeln()

########################################################################################################################
######   #######   #####   #     #  #        #######         #####   #     #  #######  ######   #     #
#     #  #        #     #  #     #  #           #           #     #  #     #  #        #     #   #   #
#     #  #        #        #     #  #           #           #     #  #     #  #        #     #    # #
######   #####     #####   #     #  #           #           #     #  #     #  #####    ######      #
#   #    #              #  #     #  #           #           #   # #  #     #  #        #   #       #
#    #   #        #     #  #     #  #           #           #    #   #     #  #        #    #      #
#     #  #######   #####    #####   #######     #            #### #   #####   #######  #     #     #
########################################################################################################################
    if ResQuery:
        _writeln("Result query:")
        ids_resu = find_element_by_regex(browser, 'id', find_execResul)
        browser.switch_to.frame(ids_resu[0])
        out_resu = browser.page_source
        csv_resu = _writesql(out_resu)
        print('%s' % csv_resu)
        browser.switch_to.default_content()
        _sleep(wait_on_step_1)
        _writeln()
        #_______________________________________________________________________________________________________________
    #CZ#_read("<press key to continue>")
        if debug_step >= 5:
            browser.save_screenshot(screenshot_tag % '3-query-2-result')
            pass

except Exception as e:
    _writeln("________________")
    _writeln("Exception Detect")
    _writeln(e)
    if browser is not None:
        browser.quit()
    #CZ#browser.close()
    if VirDisplay:
        vdisplay.stop()
    ExitCode = 1
finally:
    if ExitCode != 0:
        _writebuffer()
        sys.exit(ExitCode)

try:
########################################################################################################################
######      #      #####   #######        ######      #      #####   #    #
#     #    # #    #     #  #              #     #    # #    #     #  #   #
#     #   #   #   #        #              #     #   #   #   #        #  #
######   #     #  #  ####  #####          ######   #     #  #        ###
#        #######  #     #  #              #     #  #######  #        #  #
#        #     #  #     #  #              #     #  #     #  #     #  #   #
#        #     #   #####   #######        ######   #     #   #####   #    #
########################################################################################################################
    if PageBack:
        _write("Page back:")
    #CZ#browser.execute_script("window.history.go(-1)")
    #CZ#browser.execute_script("window.history.go(-2)")
        browser.back()
        browser.back()
        _sleep(wait_on_step_2)
        _writeln()
        #_______________________________________________________________________________________________________________
        if debug_step >= 5:
            browser.save_screenshot(screenshot_tag % '4-logout')
            pass

########################################################################################################################
######      #      #####   #######        #        #######   #####   #######  #     #  #######
#     #    # #    #     #  #              #        #     #  #     #  #     #  #     #     #
#     #   #   #   #        #              #        #     #  #        #     #  #     #     #
######   #     #  #  ####  #####          #        #     #  #  ####  #     #  #     #     #
#        #######  #     #  #              #        #     #  #     #  #     #  #     #     #
#        #     #  #     #  #              #        #     #  #     #  #     #  #     #     #
#        #     #   #####   #######        #######  #######   #####   #######   #####      #
########################################################################################################################
    if PageLogout:
        _write("Logout:")
        logout_ids = find_element_by_regex(browser, 'id', find_theLogout, 2)
        logout_attempt = browser.find_element_by_id(logout_ids[0])
        logout_attempt.click()
        _sleep(wait_on_step_1)
        _writeln()

########################################################################################################################
######   #######  #     #  ######         ######   ######   #######  #     #   #####   #######  ######
#     #  #     #  ##    #  #              #     #  #     #  #     #  #  #  #  #     #  #        #     #
#     #  #     #  # #   #  #              #     #  #     #  #     #  #  #  #  #        #        #     #
#     #  #     #  #  #  #  #####          ######   ######   #     #  #  #  #   #####   #####    ######
#     #  #     #  #   # #  #              #     #  #   #    #     #  #  #  #        #  #        #   #
#     #  #     #  #    ##  #              #     #  #    #   #     #  #  #  #  #     #  #        #    #
######   #######  #     #  ######         ######   #     #  #######   ## ##    #####   #######  #     #
########################################################################################################################
    if DoneBrowser:
        _writeln("Done browser %s." % browser_wd)
        browser.quit()
    #CZ#browser.close()

########################################################################################################################
######   #######  #     #  #######        ######   ###   #####   ######   #           #     #     #
#     #  #     #  ##    #  #              #     #   #   #     #  #     #  #          # #     #   #
#     #  #     #  # #   #  #              #     #   #   #        #     #  #         #   #     # #
#     #  #     #  #  #  #  #####          #     #   #    #####   ######   #        #     #     #
#     #  #     #  #   # #  #              #     #   #         #  #        #        #######     #
#     #  #     #  #    ##  #              #     #   #   #     #  #        #        #     #     #
######   #######  #     #  #######        ######   ###   #####   #        #######  #     #     #
########################################################################################################################
    if VirDisplay:
        vdisplay.stop()
    # _______________________________________________________________________________________________________________
    _writeln("Success :-)")

except Exception as e:
    _writeln("________________")
    _writeln("Exception Detect")
    _writeln(e)
    browser.close()
    if VirDisplay:
        vdisplay.stop()
    ExitCode = 1
    raise Exception('Error after result :-|')
finally:
    if ExitCode != 0:
        _writebuffer()
    sys.exit(ExitCode)
