#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydoc import browse

__author__ = 'zappyk'

import sys, re, time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser_wd = 'Firefox'
#browser_wd = 'PhantomJS'
#browser_wd = 'Chrome'

browser_wd_PhantomJS_screenshot = 'screenshot.png'
browser_wd_PhantomJS_htmlString = '<html><body><div style="background-color:red;height:500px;width:500px;">This is a png</div></body></html>'

user_agent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
base_path_ = "https://test.payroll.it/HRPW"
base_path_ = "https://saas.hrzucchetti.it/hrppbs"
page_home_ = base_path_ + "/HRPW/jsp/home.jsp"
page_login = base_path_ + "/jsp/login.jsp"
page_query = base_path_ + "/servlet/cost_bexecrunsql?m_cWindowName=main"
username_v = 'administrator'
password_v = '!S3rv1c3s!'
password_v = '!4cc4d3m14!'
username_t = "m_cUserName"
password_t = "m_cPassword"

type_login = "//*[@type='submit']"
exec_query = ".btsalva"              #    => find_element_by_css_selector(exec_query)
exec_query = ".*_RunButton"          # id => find_element_by_xpath("//*[@id='.*_RunButton']")
exec_resul = ".*_FrameResult"        # id => find_element_by_xpath("//*[@id='.*_FrameResult']")
exec_resul = ".*_FrameResult_iframe" # id => find_element_by_xpath("//*[@id='.*_FrameResult_iframe']")
logout_tag = ".*_imgLogouthref"      # id => find_element_by_xpath("//*[@id='.*_imgLogouthref']"")

query_area = 'MMSQL'
query_exec = 'select * from coda_001company00'

########################################################################################################################
def _write(string=''):
    print(string, end='')
    sys.stdout.flush()

########################################################################################################################
def _writeln(string=''):
    print(string)

########################################################################################################################
def _sleep(count=1, debug=0):
    debug = 2
    if debug == 1:
        _write('sleep(%s' % count)
    for i in range(0, count, 1):
        time.sleep(1)
        if debug == 1:
            _write(count -i -1)
        if debug == 2:
            _write('.')
    if debug == 1:
        _write(')')

########################################################################################################################
def _read(string=''):
    import fileinput
    _write(string)
    for input_line in fileinput.input():
        pass
    return(input_line)

########################################################################################################################
def _html_table2text(html_table=''):
    import html2text
#CZ#html_table = open("test-zi-url-4-selenium.html").read()
#CZ#text = html2text.html2text(html_table, bodywidth=130).encode('utf-8')
    text = html2text.html2text(html_table, bodywidth=300)
    return(text)

########################################################################################################################
def find_element_by_regex(bw=None, xpath='id', regex=None, debug=0):
#CZ#debug = 2
    xpa = []
    xps = bw.find_elements_by_xpath('//*[@%s]' % xpath)
    for xp in xps:
        ga = xp.get_attribute(xpath)
        if debug == 1:
            _write('find [%s]=[%s] => ' % (xpath, ga))
        if re.search(regex, ga):
            xpa.append(ga)
            if debug == 1:
                _writeln('Ok')
            if debug == 2:
                _writeln('find [%s]=[%s]' % (xpath, ga))
        else:
            if debug == 1:
                _writeln()

    return(xpa)

########################################################################################################################
def _browser(browser_webdrive):
    browser = None
    if browser_webdrive == 'Firefox':
        browser = webdriver.Firefox()
    if browser_webdrive == 'PhantomJS':
        browser = webdriver.PhantomJS()
        browser.set_window_size(1920, 1080)
        browser.get_screenshot_as_file(browser_wd_PhantomJS_screenshot)
    if browser_webdrive == 'Chrome':
        browser = webdriver.Chrome()
    if browser is None:
        _writeln('Browser %s not implemented :-(' % browser_webdrive)
        sys.exit(1)
    return(browser)

########################################################################################################################
########################################################################################################################
########################################################################################################################
_write("Open browser %s:" % browser_wd)
browser = _browser(browser_wd)
browser.get(page_login)
_sleep(3)
_writeln()

_write("Login credential:")
username = browser.find_element_by_name(username_t)
password = browser.find_element_by_name(password_t)
username.send_keys(username_v)
password.send_keys(password_v)
login_attempt = browser.find_element_by_xpath(type_login)
login_attempt.click()
_sleep(3)
_writeln()

_write("Open Page query:")
browser.get(page_query)
_sleep(3)
_writeln()

#browser.execute_script("document.write('{}');".format(browser_wd_PhantomJS_htmlString))
#browser.save_screenshot(browser_wd_PhantomJS_screenshot)

#try:
##CZ#browser.save_screenshot('screenshot.png')
##CZ#browser.get_screenshot_as_file('screenshot.png')
#    print('########################################################################################################################')
#    print(browser.page_source())
#    print('########################################################################################################################')
#except Exception as e:
#    print(e)

_write("Page alert accept:")
if browser_wd == 'Firefox'\
or browser_wd == 'Chrome':
#CZ#browser.switch_to_alert().accept()
    browser.switch_to.alert.accept()
if browser_wd == 'PhantomJS':
    browser.execute_script("window.confirm = function(msg) { return true; }")
_sleep(3)
_writeln()

_writeln("\t|\n\t| here is Insert & Execute query\n\t|")

_write("Insert query:")
sql_area = browser.find_element_by_name(query_area)
sql_area.send_keys(query_exec)
_sleep(3)
_writeln()

_write("Execute query:")
ids_exec = find_element_by_regex(browser, 'id', exec_query)
sql_exec = browser.find_element_by_id(ids_exec[0])
#print("[%s]" % sql_exec)
sql_exec.click()
_sleep(9)
_writeln()

_write("Result query:")
ids_resu = find_element_by_regex(browser, 'id', exec_resul)
browser.switch_to.frame(ids_resu[0])
#print(browser.page_source)
ps = browser.page_source
tt = _html_table2text(ps)
#print("%s" % ps)
print("%s" % tt)
browser.switch_to.default_content()
_sleep(3)
_writeln()

#_read("<press key to continue>")

_write("Back Page:")
#browser.execute_script("window.history.go(-1)")
#browser.execute_script("window.history.go(-2)")
browser.back()
browser.back()
_sleep(3)
_writeln()

_write("Logout:")
logout_ids = find_element_by_regex(browser, 'id', logout_tag)
logout_attempt = browser.find_element_by_id(logout_ids[0])
#print("[%s]" % logout_attempt)
logout_attempt.click()
_sleep(3)
_writeln()

_writeln("Close browser %s." % browser_wd)
#browser.close()
browser.quit()
_writeln("Success :-)")

sys.exit(0)