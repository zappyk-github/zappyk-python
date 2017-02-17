#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys, re

import requests

user_agent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
page_login = "https://test.payroll.it/HRPW/jsp/login.jsp"
page_home  = "https://test.payroll.it/HRPW/jsp/home.jsp"
page_query = "https://test.payroll.it/HRPW/servlet/cost_bexecrunsql?m_cWindowName=main"
username_v = 'pes0zap'
password_v = 'crl0zpp1'
username_t = "m_cUserName"
password_t = "m_cPassword"

with requests.Session() as c:
    c.get(page_login)
    print('Page Login = [%s]' % page_login)

    login_data = dict(username_t=username_v,
                      password_t=password_v) #, next='/')

    c.post(page_login, data=login_data, headers={"Referer": page_home})
    page = c.get(page_query)

    print(page.content)