# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os, re

from urllib import request

###########################################################################
def _wgetFile(url_path_file, tag_down_name):
    # Use http://www.someproxy.com:3128 for http proxying
    #proxies = {'http': 'http://www.someproxy.com:3128'}
    #filehandle = urllib.urlopen(some_url, proxies=proxies)
    # Don't use any proxies
    #filehandle = urllib.urlopen(some_url, proxies={})
    # Use proxies from environment - both versions are equivalent
    #filehandle = urllib.urlopen(some_url, proxies=None)
    #filehandle = urllib.urlopen(some_url)

    if re.match('nt|ce', os.name):
        request.getproxies_registry()
    request.urlretrieve(url_path_file, tag_down_name)