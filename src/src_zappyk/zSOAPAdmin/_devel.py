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
def main():
    #_test1_p1()
    #_test1_p2()
    #_test1_p3()
    _test1_p4()
    
    #_test2_s1()
    #_test2_s2()

#______________________________________________________________________________
def _test1_p4():
    import zeep
    
    #wsdl_url = os.environ.get('WSDL_URL')
    wsdl_url = WSDL_URL_QUERY
    soap = zeep.Client(wsdl=wsdl_url, 
                       service_name="rep_dormakaba_copiaWSService",
                       port_name="rep_dormakaba_copiaWSPort")
    #result = soap.service.Add(5, 5)
    result = soap.service.rep_dormakaba_copia_QueryResponse()
    
    #assert result == 10

#______________________________________________________________________________
def _test1_p3():
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

#______________________________________________________________________________
def _test1_p2():    
    from zeep import Client
    from zeep import xsd
    
    print("_test1_p2()")

    client = Client(WSDL_URL_QUERY) # this will use default binding
    
    print("_test1_p2() client = %s" % client)

    #client.create_message(client.service, binding_name={'m_UserName': 'pes0servizio_SOAP', 'm_Password': '%mAK:M^x1GahuaJIJq', 'm_Company': '001'}, operation_name="rep_dormakaba_copia_Query")
    client.create_message(client.service, binding_name={'m_UserName': 'pes0servizio_SOAP', 'm_Password': '%mAK:M^x1GahuaJIJq', 'm_Company': '001'}, operation_name="rep_dormakaba_copia_TabularQuery")
    
    #client.service.rep_dormakaba_copia_Query()
    client.service.rep_dormakaba_copia_TabularQuery()
    
    return
    
    #client_admin = client.bind('m_UserName', 'pes0servizio_SOAP')
    #client_admin = client_admin.bind('m_Password', '%mAK:M^x1GahuaJIJq')
    #client_admin = client_admin.bind('m_Company' , '001')
    
    #client_admin.create_service()
    #client_admin.service.rep_dormakaba_copia_Query() #this will call method1 defined in service name ServiceName and port PortNameAdmin
    #client_admin.rep_dormakaba_copia_TabularQuery() #this will call method1 defined in service name ServiceName and port PortNameAdmin

    #return

    with client.bind('m_UserName', 'pes0servizio_SOAP').settings(raw_response=True):
        #response = client.service.rep_dormakaba_copia_Query()
        response = client.service.rep_dormakaba_copia_TabularQuery()

        # response is now a regular requests.Response object
        assert response.status_code == 200
        assert response.content

#______________________________________________________________________________
def _test1_p1():
    from requests import Session
    from zeep import Client
    from zeep.cache import SqliteCache
    from zeep.transports import Transport
    from lxml import etree

    #session = Session()
    #session.cert = 'client.pem'
    #transport = Transport(session=session, cache=SqliteCache())
    #client = Client('example.wsdl', transport=transport)
    
    print("_test1_p1()")
    
    #transport = Transport(cache=SqliteCache())
    #client = Client(WSDL_URL_QUERY, transport=transport)
    client = Client(wsdl=WSDL_URL_QUERY)

    request_data = {
    'updateRecord':{
        'm_UserName': 'pes0servizio_SOAP',
        'm_Password': '%mAK:M^x1GahuaJIJq',
        'm_Company' : '001'
        }
    }
    #xml = client.create_message(client.service, 'rep_dormakaba_copia_Query', **request_data)
    xml = client.create_message(client.service, operation_name="rep_dormakaba_copiaWSService")
    
    print(etree.tostring(xml, encoding="unicode", pretty_print=True))

###############################################################################

#______________________________________________________________________________
def _test2_s2():
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

#______________________________________________________________________________
def _test2_s1():
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
# Entry point
if __name__ == '__main__':
    main()

exit(0)
