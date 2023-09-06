# -*- coding: utf-8 -*-
__author__ = 'pes0zap'

# Importing modules:
import os
import pathlib

#import SOAP_send2xml
#import SOAP_xml2csv

def die(error_message):
    raise Exception(error_message)
    exit(1)

_LINK_WEBS   = None ; _LINK_WEBS = "saas.hrzucchetti.it/Paghe3fedrigoni"
_NAME_WSDL   = None ; _NAME_WSDL =  "rep_dormakaba_copia"
_TYPE_WSDL   = None # "QUERY"
_ENVIRONMENT = None # "001"

DEFAULT_TYPE_WSDL   = "QUERY" # "REPORT"
DEFAULT_ENVIRONMENT = "001"

LINK_WEBS    = _LINK_WEBS   if _LINK_WEBS   else die("_LINK_WEBS not defined!")
NAME_WSDL    = _NAME_WSDL   if _NAME_WSDL   else die("_NAME_WSDL not defined!")
TYPE_WSDL    = _TYPE_WSDL   if _TYPE_WSDL   else DEFAULT_TYPE_WSDL
ENVIRONMENT  = _ENVIRONMENT if _ENVIRONMENT else DEFAULT_ENVIRONMENT

PATH_TEMPLATE      = "var"
NAME_SUFFIX_QUERY  = "zucchetti-SOAP-{0}-".format(TYPE_WSDL)
NAME_SUFFIX_REPORT = "zucchetti-SOAP-REPORT-"
XMLT_XML_EXTENSION = ".xmlT"
WSDL_XML_EXTENSION = ".xml"
OUT_XML_EXTENSION  = "-out.xml"
OUT_CSV_EXTENSION  = "-out.csv"

"""
WSDL_URL_QUERY  = "https://{0}/servlet/SQLDataProviderServer/SERVLET/{1}?wsdl".format(LINK_WEBS, NAME_WSDL)
WSDL_URL_REPORT = "https://{0}/servlet/Report/SERVLET/{1}?wsdl".format(LINK_WEBS, NAME_WSDL)

PATH_BASE       = pathlib.Path(__file__).parent.resolve()

XMLT_XML_QUERY  = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_QUERY , _NAME_WSDL, XMLT_XML_EXTENSION))
XMLT_XML_REPORT = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_REPORT, _NAME_WSDL, XMLT_XML_EXTENSION))

WSDL_XML_QUERY  = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_QUERY , _NAME_WSDL, WSDL_XML_EXTENSION))
WSDL_XML_REPORT = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_REPORT, _NAME_WSDL, WSDL_XML_EXTENSION))

OUT_XML_QUERY   = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_QUERY , _NAME_WSDL, OUT_XML_EXTENSION))
OUT_XML_REPORT  = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_REPORT, _NAME_WSDL, OUT_XML_EXTENSION))

OUT_CSV_QUERY   = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_QUERY , _NAME_WSDL, OUT_CSV_EXTENSION))
OUT_CSV_REPORT  = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_REPORT, _NAME_WSDL, OUT_CSV_EXTENSION))

ADD_XML_VERSION = '<?xml version="1.0" encoding="utf-8"?>'
"""

class admin(object):
    wsdl_url = None
    wsdl_xml = None
    out_xml = None
    out_csv = None
    
    WSDL_URL_QUERY  = "https://{0}/servlet/SQLDataProviderServer/SERVLET/{1}?wsdl".format(LINK_WEBS, NAME_WSDL)
    WSDL_URL_REPORT = "https://{0}/servlet/Report/SERVLET/{1}?wsdl".format(LINK_WEBS, NAME_WSDL)
    
    PATH_BASE       = pathlib.Path(__file__).parent.resolve()

    XMLT_XML_QUERY  = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_QUERY , _NAME_WSDL, XMLT_XML_EXTENSION))
    XMLT_XML_REPORT = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_REPORT, _NAME_WSDL, XMLT_XML_EXTENSION))

    WSDL_XML_QUERY  = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_QUERY , _NAME_WSDL, WSDL_XML_EXTENSION))
    WSDL_XML_REPORT = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_REPORT, _NAME_WSDL, WSDL_XML_EXTENSION))

    OUT_XML_QUERY   = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_QUERY , _NAME_WSDL, OUT_XML_EXTENSION))
    OUT_XML_REPORT  = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_REPORT, _NAME_WSDL, OUT_XML_EXTENSION))

    OUT_CSV_QUERY   = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_QUERY , _NAME_WSDL, OUT_CSV_EXTENSION))
    OUT_CSV_REPORT  = os.path.join(PATH_BASE, PATH_TEMPLATE, "{0}{1}{2}".format(NAME_SUFFIX_REPORT, _NAME_WSDL, OUT_CSV_EXTENSION))

    ADD_XML_VERSION = """<?xml version="1.0" encoding="utf-8"?>"""

    def __init__(self, wsdl_url, wsdl_xml, out_xml, out_csv):
        self.wsdl_url = wsdl_url
        self.wsdl_xml = wsdl_xml
        self.out_xml = out_xml
        self.out_csv = out_csv

    def __init__(self):
        self.__init__(self.WSDL_URL_QUERY, self.WSDL_XML_QUERY, self.OUT_XML_QUERY, self.OUT_CSV_QUERY)

def main():
    cfg = admin()
    #cfg = admin(WSDL_URL_QUERY, WSDL_XML_QUERY, OUT_XML_QUERY, OUT_CSV_QUERY)
    print("Init:")
    print(cfg)
    print(cfg.PATH_BASE)
    print("Done.")
    
def die(error_message):
    raise Exception(error_message)

# Entry point
if __name__ == '__main__':
    main()

exit(0)