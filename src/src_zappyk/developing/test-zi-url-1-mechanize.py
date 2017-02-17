#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys
import cookielib
import urllib3
import mechanize

user_agent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
page_login = "https://test.payroll.it/HRPW/jsp/login.jsp"
page_query = "https://test.payroll.it/HRPW/servlet/cost_bexecrunsql?m_cWindowName=main"
username_v = 'pes0zap'
password_v = 'crl0zpp1'
username_t = "m_cUserName"
password_t = "m_cPassword"

# Browser
br = mechanize.Browser()

# Enable cookie support for urllib2
cookiejar = cookielib.LWPCookieJar()
br.set_cookiejar(cookiejar)

# Broser options
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# ??
br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 )

br.addheaders = [('User-agent', user_agent)]

# authenticate
br.open(page_login)
print('Page Login = [%s]' % page_login)

form_login = None
#for form in br.forms():
#    form_login = form.name
#    print 'Form Login = [%s]' % form_login
form_login = list(br.forms())[0].name
print('Form Login = [%s]' % form_login)

br.select_form(name=form_login)
print(br.form)
print(type(br.form))
print('mylink=[%s]' % br.form["mylink"])
print('TITOLO=[%s]' % br.form["TITOLO"])
print('m_cAction=[%s]' % br.form["m_cAction"])
print('m_cURL=[%s]' % br.form["m_cURL"])
print('m_cURLOnError=[%s]' % br.form["m_cURLOnError"])
sys.exit(0)
# these two come from the code you posted
# where you would normally put in your username and password
br.form[username_t] = username_v
br.form[password_t] = password_v
res = br.submit()

print(res)
print("Success!")

#br.open(page_query)
#res = br.submit()

print(res)
print("Open?")

sys.exit(0)