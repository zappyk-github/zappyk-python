#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'
########################################################################################################################
from O365 import Account

auth_flow_CREDENTIALS = 'credentials'
auth_flow_AUTHORIZATION = 'authorization'

tenant_id = '8880a91d-ce48-4314-9921-359b8a3d83a3' # P&S Payroll Services

#credentials = ('e71c20d5-7cae-4cda-aec7-63439e7dea80', 'ejdUTX9564~[)ttncLYBB2$') # Webexe connector
credentials = ('f2313123-255b-4d30-bd85-77529b9d887d', 'ZAtz1zzhK-0-nGSr.CDD5qBOy1-82OcU43') # PeS connector, expire 17/04/2023

auth_flow_s = auth_flow_CREDENTIALS
#auth_flow_s = auth_flow_AUTHORIZATION

scopes_list = None
if (auth_flow_s == auth_flow_CREDENTIALS):
    scopes_list = None
if (auth_flow_s == auth_flow_AUTHORIZATION):
    scopes_list = ['basic', 'message_all']

account = Account(credentials, tenant_id=tenant_id, auth_flow_type=auth_flow_s)
account.authenticate(scopes=scopes_list)
print("Authenticate is %s" % account.is_authenticated)
#exit(1)

m = account.new_message()
m.to.add('pes0zap@payroll.it')
m.subject = 'Testing!'
m.body = "George Best quote: I've stopped drinking, but only while I'm asleep."
m.send()

exit(0)
