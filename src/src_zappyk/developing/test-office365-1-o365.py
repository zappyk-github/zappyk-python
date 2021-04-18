#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'
########################################################################################################################
import os

from O365 import Account, FileSystemTokenBackend, MSOffice365Protocol, MSGraphProtocol

auth_flow_type_AUTHORIZATION = 'authorization'
auth_flow_type_CREDENTIALS = 'credentials'
auth_flow_type_PUBLIC = 'public'

tenant_id = '8880a91d-ce48-4314-9921-359b8a3d83a3' # P&S - Payroll Services

token_backend = FileSystemTokenBackend(token_path=os.getcwd()+'/resources/test-office365-1-o365.tokens/', token_filename='o365_token.my.txt')
#credentials = ('e71c20d5-7cae-4cda-aec7-63439e7dea80', 'ejdUTX9564~[)ttncLYBB2$')           # Webexe connector, not expired
credentials = ('f2313123-255b-4d30-bd85-77529b9d887d', 'ZAtz1zzhK-0-nGSr.CDD5qBOy1-82OcU43') # PeS connector, expired 17/04/2023

auth_flow_type = auth_flow_type_AUTHORIZATION
auth_flow_type = auth_flow_type_CREDENTIALS
#auth_flow_type = auth_flow_type_PUBLIC

scopes_list = None
if (auth_flow_type == auth_flow_type_AUTHORIZATION):
    scopes_list = ['basic', 'message_all'] # ['User.Read'] + ['Mail.ReadWrite', 'Mail.Send']
    scopes_list = ['message_all']          # ['Mail.ReadWrite', 'Mail.Send']
    scopes_list = ['message_send']         # ['Mail.Send']
    #scopes_list = ['basic', 'message_send']
if (auth_flow_type == auth_flow_type_CREDENTIALS):
    scopes_list = None
    #scopes_list = ['https://graph.microsoft.com/Mail.ReadWrite', 'https://graph.microsoft.com/Mail.Send']
    #scopes_list = ['https://graph.microsoft.com/Mail.Send']
    #scopes_list = ['basic', 'message_send']
    #protocol_graph = MSGraphProtocol(api_version='')
    #protocol_graph = MSGraphProtocol()
    #scopes_list = protocol_graph.get_scopes_for(['basic', 'message_send'])
    #scopes_list = protocol_graph.get_scopes_for(['message_send'])
if (auth_flow_type == auth_flow_type_PUBLIC):
    scopes_list = None
    #scopes_list = ["https://graph.microsoft.com/.default"]

""""
protocol_office = MSOffice365Protocol()
scopes_office = protocol_office.get_scopes_for('message all')
print(protocol_office)
print(scopes_office)

protocol_graph = MSGraphProtocol()
scopes_graph = protocol_graph.get_scopes_for('message all')
print(protocol_graph)
print(scopes_graph)
"""

print("Scopes: %s" % scopes_list)

account = Account(credentials, tenant_id=tenant_id, auth_flow_type=auth_flow_type, token_backend=token_backend, scopes=scopes_list)
account_authenticate = account.authenticate()
print("Authenticated is %s (authenticate %s)" % (account.is_authenticated, account_authenticate))
if not(account.is_authenticated) or not(account_authenticate):
    exit(1)
print("Account connection: %s" % account.connection)

"""
print("Try send e-mail...")
mb = account.mailbox(resource='pes0zap@payroll.it')
nm = mb.new_message()
nm.to.add('pes0zap@payroll.it')
nm.subject = 'Testing!'
nm.body = "George Best quote: I've stopped drinking, but only while I'm asleep."
nm.send()
"""

print("Try teams...")
t = account.teams(resource='pes0zap@payroll.it')
print(t.new_query())

print("End!")
exit(0)
