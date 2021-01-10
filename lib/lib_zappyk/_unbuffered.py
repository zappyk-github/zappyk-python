# -*- coding: utf-8 -*-
__author__ = 'zappyk'

###########################################################################
class Unbuffered(object):

   def __init__(self, stream):
       self.stream = stream

   def write(self, data):
       self.stream.write(data)
       self.stream.flush()

   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()

   def __getattr__(self, attr):
       return getattr(self.stream, attr)

###########################################################################
#
# You can skip buffering for a whole python process using
#     "python -u"     (or #!/usr/bin/env python -u etc)
# or by setting the environment variable PYTHONUNBUFFERED
#
# You could also replace sys.stdout with some other stream
# like wrapper which does a flush after every call.
#
###########
# EXAMPLE #
#_________#________________________________________________________________
# import sys
# sys.stdout = Unbuffered(sys.stdout)
# print('Hello')
