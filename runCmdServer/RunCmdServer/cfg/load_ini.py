# -*- coding: utf-8 -*-
import os
###############################################################################
_Os_path_join = os.path.sep
###############################################################################
server_socket_host = ''
server_socket_port = 10000
#server_chunks_recv= 16
#server_chunks_recv= 256
server_chunks_recv = 1024
server_set_timeout = 0
server_one_process = True
###############################################################################
client_socket_host = ''
client_socket_port = 10001
client_chunks_recv = server_chunks_recv
client_set_timeout = 1800
################################################################################