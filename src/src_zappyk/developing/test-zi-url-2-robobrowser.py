#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys, re

from robobrowser import RoboBrowser

user_agent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
page_login = "https://test.payroll.it/HRPW/jsp/login.jsp"
page_query = "https://test.payroll.it/HRPW/servlet/cost_bexecrunsql?m_cWindowName=main"
username_v = 'pes0zap'
password_v = 'crl0zpp1'
username_t = "m_cUserName"
password_t = "m_cPassword"

########################################################################################################################
def _to_string(line):
    return(str(line).split("\n"))

########################################################################################################################
browser = RoboBrowser(
    history=True,
    user_agent=user_agent
)

browser.open(page_login)
print('Page Login = [%s]' % page_login)

login_form = None
#for line in str(browser.find_all()[0]).split("\n"):
for line in _to_string(browser.find_all()[0]):
    m = re.search(r""".*form\s*id="(\w*)"\s*method=.*""", line)
    if m:
        login_form = m.group(1)
print('Form Login = [%s]' % login_form)

form = browser.get_form(id=login_form)
form[username_t].value = username_v
form[password_t].value = password_v
browser.submit_form(form)
print("Success!")

browser.open("https://test.payroll.it/HRPW/servlet/cost_bexecrunsql?m_cWindowName=main")
print("Open?")
print(_to_string(browser.find_all()[0]))

sys.exit(0)