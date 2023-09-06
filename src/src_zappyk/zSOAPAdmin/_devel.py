# -*- coding: utf-8 -*-
__author__ = 'pes0zap'

# Importing modules:
import os
import re
import sys
import csv
import pathlib
import shutil

WSDL_URL_QUERY  = "https://saas.hrzucchetti.it/Paghe3fedrigoni/servlet/SQLDataProviderServer/SERVLET/rep_dormakaba_copia?wsdl"
WSDL_URL_REPORT = "https://saas.hrzucchetti.it/Paghe3fedrigoni/servlet/Report/SERVLET/rep_dormakaba_copia?wsdl"

WSDL_XML_QUERY  = os.path.join(pathlib.Path(__file__).parent.resolve(), "resources", "rep_dormakaba_copia-QUERY.xml")
WSDL_XML_REPORT = os.path.join(pathlib.Path(__file__).parent.resolve(), "resources", "rep_dormakaba_copia-REPORT.xml")

OUT_XML_QUERY  = os.path.join(pathlib.Path(__file__).parent.resolve(), "resources", "rep_dormakaba_copia-QUERY-out.xml")
OUT_XML_REPORT = os.path.join(pathlib.Path(__file__).parent.resolve(), "resources", "rep_dormakaba_copia-REPORT-out.xml")

OUT_CSV_QUERY  = os.path.join(pathlib.Path(__file__).parent.resolve(), "resources", "rep_dormakaba_copia-QUERY-out.csv")
OUT_CSV_REPORT = os.path.join(pathlib.Path(__file__).parent.resolve(), "resources", "rep_dormakaba_copia-REPORT-out.csv")

xml_version = '<?xml version="1.0" encoding="utf-8"?>'

###############################################################################

from zeep import Client
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth
#wsdl = URL_QUERY
#session = Session()
#print("Session: %s" % session)
#print("Session .get: %s" % session.get)
#for s in session:
#    print("s: %s" % s)

#session.auth = HTTPBasicAuth(<username>, <password>)
#client = Client(wsdl,transport=Transport(session=session))

#request_data={'SAPUsername' : SAP_username ,
#              'SAPPassword' : SAP_password}

#client = Client(URL_QUERY)
#print("Client: %s" % client)
#print("Client.wsdl.dump: %s" % client.wsdl.dump())
#for c in client:
#    print("c: %s" % c)

#service = client.bind("m_UserName", "pes0servizio_SOAP")
#service = client.bind("m_Password", "%mAK:M^x1GahuaJIJq")
#service = client.bind("m_Company", "001")
#service.method1()

#node = client.create_message(client.service, 'myOperation', user='hi')
#print(node)

###############################################################################

import requests

# SOAP request URL
url = WSDL_URL_QUERY
  
# structured XML
#open text file in read mode
text_file = open(WSDL_XML_QUERY, "r")
#read whole file to a string
data = text_file.read()
#close file
text_file.close()

# structured XML
payload = data

# headers
headers = { 'Content-Type': 'text/xml; charset=utf-8' }
# POST request
response = requests.request("POST", url, headers=headers, data=payload)

# prints the response
#print(response.text)
#print("-------------------------------------------------------------------------------")
#print(response)

###############################################################################

import xml.etree.ElementTree as ET

#xml_elements = ET.XML("<html><body>text</body></html>")
xml_elements = ET.XML(response.text)
ET.indent(xml_elements)
#print(ET.tostring(element, encoding='unicode'))
file_object = open(OUT_XML_QUERY, "w")
file_object.write(ET.tostring(xml_elements, encoding='unicode'))
file_object.close()
#exit(0)

out_csv_count = 0
out_csv_lines = []
out_csv_head = []
out_csv_line = {}

try:
    #mytree = ET.fromstring(response.text)
    #print(xml_elements)
    #mytree = xml_elements
    mytree = ET.parse(OUT_XML_QUERY)
    print(mytree)
    for myelem in mytree.iter():
    #for myelem in mytree.findall("**//Records/item"):
        #print(myelem)
        print("%s: '%s'" % (myelem.tag, myelem.text))
        
        field = re.sub(r"""^{.*}""", "", myelem.tag)
        value = "" if myelem.text == None else myelem.text.strip()
        
        if field == 'item':
            out_csv_count += 1
            out_csv_lines.append(out_csv_line)
            out_csv_line = {}
        else:
            out_csv_line[field]= value
            if out_csv_count == 1:
                out_csv_head.append(field)
            #if out_csv_count == 1:
            #    out_csv_line.append(field)
            #else:
            #    out_csv_line.append(value)
    if out_csv_line:    
        out_csv_lines.append(out_csv_line)
except:
    print("...error 1...")

try:
    count = 0
    print("-------------------------------------------------------------------------------")
    print(out_csv_head)
    with open(OUT_CSV_QUERY, "w", newline='') as csvfile:
        #spamwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        writer = csv.DictWriter(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=out_csv_head)
        writer.writeheader()
        for out_csv_line in out_csv_lines:
            print(out_csv_line)
            
            #spamwriter.writerow(out_csv_line)
            
            try:
                writer.writerow(out_csv_line)
            except:
                print("skip: %s" % out_csv_line)
except:
    print("...error 2...")

exit(0)

###############################################################################