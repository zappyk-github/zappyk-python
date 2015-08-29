# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import sys
import json
import socket
import datetime

from lib_zappyk._os      import _os

from runCmdServer.RunCmdServer.cfg.load_cfg  import parser_args, parser_conf, logger_conf
from runCmdServer.RunCmdServer.cfg.load_ini  import *
from runCmdServer.RunCmdServer.src.constants import *

args = parser_args().args
conf = parser_conf().conf
logs = logger_conf().logs

server_socket_host = conf.get       ("Server"  , "server_socket_host", fallback=server_socket_host)
server_socket_port = conf.getint    ("Server"  , "server_socket_port", fallback=server_socket_port)
server_chunks_recv = conf.getint    ("Server"  , "server_chunks_recv", fallback=server_chunks_recv)
server_set_timeout = conf.getint    ("Server"  , "server_set_timeout", fallback=server_set_timeout)
server_one_process = conf.getboolean("Server"  , "server_one_process", fallback=server_one_process)

client_socket_host = conf.get       ("Client"  , "client_socket_host", fallback=client_socket_host)
client_socket_port = conf.getint    ("Client"  , "client_socket_port", fallback=client_socket_port)
client_chunks_recv = conf.getint    ("Client"  , "client_chunks_recv", fallback=client_chunks_recv)
client_set_timeout = conf.getint    ("Client"  , "client_set_timeout", fallback=client_set_timeout)

if args.server_host      is not None:  server_socket_host = args.server_host
if args.server_host_port is not None:  server_socket_port = args.server_host_port
if args.client_host      is not None:  client_socket_host = args.client_host
if args.client_host_port is not None:  client_socket_port = args.client_host_port

if client_socket_port == 0:
    client_socket_port = server_socket_port +1

if server_set_timeout == 0:
    server_set_timeout = None

if client_set_timeout == 0:
    client_set_timeout = None

server_connect        = (server_socket_host, server_socket_port)
client_connect        = (client_socket_host, server_socket_port)
server_client_connect = None
client_server_connect = (server_socket_host, client_socket_port)

server_command_run = args.remote_command

debug_internal = False

timestamp_pid = None

###############################################################################
def undo(command_exec, client_address):
    global client_socket_host
    global client_socket_port
    (client_socket_host
    ,client_socket_port
    ,command_exec) = _undo(command_exec)

    global client_connect
    client_connect        = (client_socket_host, server_socket_port)
    global client_server_connect
    client_server_connect = (client_address[0], client_socket_port)

    return(command_exec)

###############################################################################
def make():
    global server_command_run
    server_command_run = _make(client_socket_host
                              ,client_socket_port
                              ,args.remote_command)

###############################################################################
def init():
    global debug_internal
    if args.debug >= 1:
        debug_internal = True

    if args.debug >= 2:
        _log_warn("* server_socket_host = [%s]" % server_socket_host)
        _log_warn("* server_socket_port = [%s]" % server_socket_port)
        _log_warn("* server_chunks_recv = [%s]" % server_chunks_recv)
        _log_warn("* server_set_timeout = [%s]" % server_set_timeout)
        _log_warn("* server_one_process = [%s]" % server_one_process)

        _log_warn("* server_command_run = [%s]" % server_command_run)

        _log_warn("* client_socket_host = [%s]" % client_socket_host)
        _log_warn("* client_socket_port = [%s]" % client_socket_port)
        _log_warn("* client_chunks_recv = [%s]" % client_chunks_recv)
        _log_warn("* client_set_timeout = [%s]" % client_set_timeout)

        _log_warn("* debug_internal     = [%s]" % debug_internal)

    if args.debug >= 3:
        sys.exit(0)

    make()

###############################################################################
def main():

    init()

    if debug_internal:

        if args.run == RUN_SERVER: _run_server()
        if args.run == RUN_CLIENT: _run_client()

    else:

        if args.run == RUN_SERVER:
            try:
                _run_server()
            except KeyboardInterrupt:
                _log_view("")
                _log_warn("Ok, stop everything, you're the boss :-)")
            except (OSError
                   ,ConnectionRefusedError):
                exc_type, exc_value, exc_traceback = sys.exc_info()
                _log_warn("Connection Client/Server failed: %s" % exc_value)
            except SystemExit:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                _log_fail("Execute process fork ended: %s" % exc_value, exit_code=exc_value)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                _log_warn("Something did not go the right way :-(")
                _log_fail("Error: %s" % exc_value, exit_code=exc_value)

        if args.run == RUN_CLIENT:
            try:
                _run_client()
            except KeyboardInterrupt:
                _log_view("")
                _log_warn("Oops, we were still joking?! :-|")
            except (OSError
                   ,ConnectionRefusedError):
                exc_type, exc_value, exc_traceback = sys.exc_info()
                _log_warn("Connection Server/Client failed: %s" % exc_value)
        #CZ#except:
        #CZ#    exc_type, exc_value, exc_traceback = sys.exc_info()
        #CZ#    if exc_value == 0:
        #CZ#        _log_fail("Server ended ok :-)", exit_code=exc_value)
        #CZ#    else:
        #CZ#        _log_warn("Something did not go the right way :-(")
        #CZ#        _log_fail("Error: %s" % exc_value, exit_code=exc_value)

###############################################################################
def _run_command(command_exec):
    _log_noty("Execute command:")
    (command_exit
    ,command_logs) = _os._command(command_exec)
    _log_noty("Execute command done [%s]" % command_exit)
    return(command_exit, command_logs)

###############################################################################
def _run_server(sock=None):
    if sock is None:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        _log_noty("Starting up Server on %s port %s" % server_connect)
        # Bind the socket to the port
        sock.bind(server_connect)
        sock.settimeout(server_set_timeout)

        # Listen for incoming connections
        sock.listen(1)

    while True:
        # Wait for a connection
        _log_noty("Waiting max second %s for a connection..." % server_set_timeout)
        _log_seps()
        connection, client_address = sock.accept()

        command_exec = None

        try:
            _log_info("Connection from %s" % str(client_address))

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(server_chunks_recv).decode()
                if data:
                #CZ#_log_info("Received %d byte: [%s]" % (server_chunks_recv, repr(data)))
                    _log_info("Received %d byte: [%s]" % (server_chunks_recv, data))

                    _log_info("Sending data back to the client...")
                    connection.sendall(data.encode())

                    if command_exec is None:
                        command_exec = data
                    else:
                        command_exec += data

                else:
                    _log_info("No more data from %s" % str(client_address))
                    break

        finally:
            # Clean up the connection
            connection.close()
            _log_info("Closing connection")

        command_exec = undo(command_exec, client_address)

    #CZ#if command_exec is not None:
        if server_one_process:
            (command_exit
            ,command_logs) = _run_command(command_exec)
            _run_server_client(client_address[0], command_exit, command_logs)
        else:
            _os._flush_stdAll()

            command_pid = os.fork()

            if command_pid != 0:
                global timestamp_pid
                timestamp_pid = command_pid

        #CZ#if command_pid == 0:
            if command_pid != 0:
                _log_noty("Execute process fork...")
                (command_exit
                ,command_logs) = _run_command(command_exec)
                _run_server_client(client_address[0], command_exit, command_logs)

                # Clean up the connection
                connection.close()
                _log_noty("Closing connection fork")

            #CZ#sys.exit(command_exit)
            #CZ#return()
                break
        #CZ#else:
        #CZ#    global timestamp_pid
        #CZ#    timestamp_pid = command_pid
        #CZ##CZ#_run_server(sock)

        #CZ#_run_server_client(client_address[0], command_exit, command_logs)

###############################################################################
def _run_client():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    _log_noty("Connecting to Server %s port %s" % client_connect)
    sock.connect(client_connect)

    try:
        # Send data
        data = server_command_run
        _log_info("Sending [%s]" % data)
        sock.sendall(data.encode())

        # Look for the response
        amount_received = 0
        string_received = None
        amount_expected = len(data)

        while amount_received < amount_expected:
            data = sock.recv(client_chunks_recv).decode()
            amount_received += len(data)
        #CZ#_log_info("Received %d byte: [%s]" % (client_chunks_recv, repr(data)))
            _log_info("Received %d byte: [%s]" % (client_chunks_recv, data))

            if data:
                if string_received is None:
                    string_received = data
                else:
                    string_received += data

    finally:
        # Clean up the socket
        sock.close()
        _log_info("Closing socket")

    _run_client_server()
#CZ#try:
#CZ#    _run_client_server()
#CZ#except:
#CZ#    _log_warn()


###############################################################################
def _run_server_client(client_socket_host, command_exit, command_logs):
    server_client_connect = (client_socket_host, client_socket_port)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # Connect the socket to the port where the server is listening
    _log_noty("Connecting to Server/Client %s port %s" % server_client_connect)
    sock.connect(server_client_connect)

    string_received = None

    try:
        json_struct = { TAG_COMMAND_EXIT:command_exit, TAG_COMMAND_LOGS:command_logs }
        json_string = json.dumps(json_struct)

        # Send data
        data = json_string
        if debug_internal:
            _log_info("Sending [%s]" % data)
        else:
            _log_info("Sending...")
        sock.sendall(data.encode())

        # Look for the response
        amount_received = 0
        amount_expected = len(data)

        while amount_received < amount_expected:
            data = sock.recv(client_chunks_recv).decode()
            amount_received += len(data)
            if debug_internal:
            #CZ#_log_info("Received %d byte: [%s]" % (client_chunks_recv, repr(data)))
                _log_info("Received %d byte: [%s]" % (client_chunks_recv, data))
            else:
                _log_info("Received %d byte...")

            if data:
                if string_received is None:
                    string_received = data
                else:
                    string_received += data

    finally:
        # Clean up the socket
        sock.close()
        _log_info("Closing socket")
        _log_noty("Connecting to Server/Client completed!")

    if string_received is not None:
        if debug_internal:
            _log_info("Send command logs:")
            _log_view(string_received)
        else:
            _log_info("Send command logs...")

###############################################################################
def _run_client_server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    _log_noty("Starting up Client/Server on %s port %s" % client_server_connect)
    # Bind the socket to the port
    sock.bind(client_server_connect)
    sock.settimeout(client_set_timeout)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        _log_noty("Waiting max second %s for a connection..." % client_set_timeout)
    #CZ#_log_seps()
        connection, client_address = sock.accept()

        command_exec = None

        try:
            _log_info("Connection from %s" % str(client_address))

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(client_chunks_recv).decode()
                if data:
                    if debug_internal:
                    #CZ#_log_info("Received %d byte: [%s]" % (client_chunks_recv, repr(data)))
                        _log_info("Received %d byte: [%s]" % (client_chunks_recv, data))
                    else:
                        _log_info("Received %d byte..." % client_chunks_recv)

                    _log_info("Sending data back to the client...")
                    connection.sendall(data.encode())

                    if command_exec is None:
                        command_exec = data
                    else:
                        command_exec += data

                else:
                    if debug_internal:
                        _log_info("No more data from %s" % str(client_address))
                    break

        finally:
            # Clean up the connection
            connection.close()
            _log_info("Closing connection")
            _log_noty("Starting up Client/Server finished!")


        # Clean up the socket
        sock.close()
        _log_info("Closing socket")

        if command_exec is not None:
            json_struct = json.loads(command_exec)

            command_exit = json_struct[TAG_COMMAND_EXIT]
            command_logs = json_struct[TAG_COMMAND_LOGS]

            _log_noty("Return command logs:")
            _log_view(command_logs)
            _log_noty("Return command done [%s]" % command_exit)

            sys.exit(command_exit)

###############################################################################
def _make(host, port, command):
    string = URI_FORMAT % (host, port, command)
    return(string)

###############################################################################
def _undo(string):
    (host_port, command) = string.split(URI_CHARrc)
    (host, port)         = host_port.split(URI_CHARhp)
    port = int(port)
    return(host, port, command)

###############################################################################
def _pid_view(timestamp_run=''):
    if server_one_process:
        pass
    else:
        global timestamp_pid
        if timestamp_pid is None:
            timestamp_run += TAG_SERPID % ('', '')
        else:
            timestamp_run += TAG_SERPID % (TAG_SEPPID, str(timestamp_pid))
    return(timestamp_run)

###############################################################################
def _tag_view(string):
    timestamp_now = datetime.datetime.now()
    timestamp_tag = timestamp_now.strftime(NOW_FORMAT)
#CZ#timestamp_run = args.run
    timestamp_run = _pid_view(args.run)
    return(TAG_FORMAT % (TAG_LOG_CHAR, timestamp_tag, timestamp_run, string))

###############################################################################
def _log_info(string, view_force=False):
    if view_force or args.verbose:
        logs.info(_tag_view(string))
###############################################################################
def _log_seps():
    logs.info(TAG_LOG_CHAR * TAG_LOG_LENG)
###############################################################################
def _log_view(string):
    logs.info(string)
###############################################################################
def _log_noty(string):
    _log_info(string, True)
###############################################################################
def _log_warn(string):
    logs.warning(_tag_view(string))
###############################################################################
def _log_fail(string, exit_code=1):
    logs.error(_tag_view(string), exit_code=exit_code)