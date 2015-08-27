# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os, re, sys, platform, getpass, subprocess, shlex

###############################################################################
_os_linux   = False
_os_windows = False
if hasattr(os, 'statvfs'):  # POSIX
    _os_linux = True
elif os.name == 'nt':       # Windows
    _os_windows = True

###############################################################################
_os_host_name = 'unknown'
_os_host_type = 'unknown'
if _os_linux:
    _os_host_type = platform.uname()[0]
    _os_host_name = platform.uname()[1]
#CZ#_os_host_name = os.uname()[1]
elif _os_windows:
    _os_host_type = platform.uname()[0]
    _os_host_name = platform.uname()[1]

###############################################################################
class _os:
    ###########################################################################
    def _exit(exit_code):
        # os._exit whitout except! :-)
        os._exit(exit_code)
    ###########################################################################
    def _search(os_regexp):
        if re.search(os_regexp, os.name):
            return(True)
        else:
            return(False)
    ###########################################################################
    def _print_command(command):
        tag = "(%s:%s)# " % (getpass.getuser(), os.path.realpath(os.path.curdir))
        print("%s%s" % (tag, command))
    ###########################################################################
    def _system(command):
    #CZ#_os._print_command(command)
        exit_code = os.system(command)
        return(exit_code)
    ###########################################################################
    def _popen(command):
    #CZ#_os._print_command(command)

        command_exit = None
        command_stdo = None
        command_stde = None

        command_split = shlex.split(command)
        try:
        #CZ#command_proc = subprocess.Popen(command      , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            command_proc = subprocess.Popen(command_split, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            command_exit = command_proc.returncode
        #CZ#command_exit = command_proc.wait()
            command_stdo,\
            command_stde = command_proc.communicate()

            (command_exit
            ,command_stdo
            ,command_stde) = _os._popen_normalize(command_exit, command_stdo, command_stde)

            if command_exit < 0:
                print('Child was terminated by signal', -command_exit, file=sys.stderr)
        #CZ#else:
        #CZ#    print('Child retuned', command_exit, file=sys.stdout)
        except OSError as e:
            '''
            exc_type, exc_value, exc_traceback = sys.exc_info()

            print("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

            print("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)

            print("*** print_exc:")
            traceback.print_exc()

            print("*** format_exc, first and last line:")
            formatted_lines = traceback.format_exc().splitlines()
            print(formatted_lines[0])
            print(formatted_lines[-1])

            print("*** format_exception:")
            print(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            print("*** extract_tb:")
            print(repr(traceback.extract_tb(exc_traceback)))

            print("*** format_tb:")
            print(repr(traceback.format_tb(exc_traceback)))

            print("*** tb_lineno:", exc_traceback.tb_lineno)
            '''
            print('Execution OSError: %s' % e, command_exit, file=sys.stderr)
            raise(Exception(sys.exc_info()))
        except Exception as e:
            print('Execution failed: %s' % e, command_exit, file=sys.stderr)
            raise(Exception(sys.exc_info()))

        (command_exit
        ,command_stdo
        ,command_stde) = _os._popen_normalize(command_exit, command_stdo, command_stde)

        return((command_exit, command_stdo, command_stde))
    ###########################################################################
    def _popen_normalize(return_code=None, return_stdo=None, return_stde=None):
        if return_code is None:
            return_code = 0

        if return_stdo is None:
            return_stdo = ''
        else:
            if not isinstance(return_stdo, str):
            #CZ#return_stdo = return_stdo.decode(encoding='utf-8')
                return_stdo = return_stdo.decode()

        if return_stde is None:
            return_stde = ''
        else:
            if not isinstance(return_stde, str):
            #CZ#return_stde = return_stde.decode(encoding='utf-8')
                return_stde = return_stde.decode()

        return(return_code, return_stdo, return_stde)
    ###########################################################################
    # if use multiprocessing with _command_process
#CZ#def _command(command_exec, process_rtrn=None):
    def _command(command_exec=None):
        if command_exec is None:
            print("Command execute is not defined!", file=sys.stderr)
            raise()

        command_exec = command_exec.strip()
        if command_exec == '':
            print("Command execute is empty!", file=sys.stderr)
            raise()

        command_exit = 0
        command_logs = ''

        try:
        #CZ#(return_code) = _os._system(commands_open)
            (return_code
            ,return_stdo
            ,return_stde) = _os._popen(command_exec)

            command_exit = return_code
            if return_stdo != '':
                command_logs = "\n".join((command_logs, return_stdo))
            if return_stde != '':
                command_logs = "\n".join((command_logs, return_stde))

        except Exception as e:
            command_exit = 1
            command_logs = str(e)

    #CZ#if process_rtrn is not None:
    #CZ#    process_rtrn.put(command_exit)
    #CZ#    process_rtrn.put(command_logs)

        return(command_exit, command_logs)
    ###########################################################################
    def _command_process(command_exec, server_queued_fifo=[]):
        import multiprocessing, time

        process_ret = multiprocessing.Queue()
        process_run = multiprocessing.Process(target=_os._command, args=(command_exec, process_ret))
    #CZ#process_run = threading.Thread(target=_os._command, args=(command_exec, process_ret))

        server_queued_fifo.append(process_run)

        process_run.start()
        process_pid = process_run.pid

    #CZ#while process_run.is_alive():
    #CZ#    time.sleep(1)

        process_run.join()

    #CZ#command_exit = process_run.exitcode
        command_exit = process_ret.get()
        command_logs = process_ret.get()

        return(command_exit, command_logs)

    ###########################################################################
    def _flush_stdAll(self=None):
        _os._flush_stdin()
        _os._flush_stdout()
        _os._flush_stderr()
    ###########################################################################
    def _flush_stdOutErr(self=None):
        _os._flush_stdout()
        _os._flush_stderr()
    ###########################################################################
    def _flush_stdin(self=None):
        sys.stdin.flush()
    ###########################################################################
    def _flush_stdout(self=None):
        sys.stdout.flush()
    ###########################################################################
    def _flush_stderr(self=None):
        sys.stderr.flush()
    ###########################################################################
    def _clear(self=None):
        if   _os._search('nt|ce|java'):
            _os._system('cls')
            print('\r', end='')
        elif _os._search('posix|riscos|os2'):
            _os._system('clear')