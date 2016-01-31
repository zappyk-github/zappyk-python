# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os, sys, platform, subprocess, datetime

# from setuptools          import setup
# from distutils.core      import setup, Extension
# from distutils.sysconfig import get_python_lib

from setuptools import find_packages
from cx_Freeze  import setup, Executable

AUTHOR       = __author__
AUTHOR_EMAIL = 'zappyk@gmail.com'
LICENSE      = 'BSD'
URL          = 'http://plus.google.com/u/0/+CarloZappacosta/'

_language_name = 'python'

_build_exe_char_seps = '_'
_build_exe_name_seps = '-'
_build_exe_path_init = 'exe.'
_build_exe_path_base = ['build']

###############################################################################
def _setup(**options):
    setup(**options)

###############################################################################
def _find_packages(**options):
    find_packages(**options)

###############################################################################
def _setup_Executable(file_execute, **options):
    return(Executable(file_execute, **options))

###############################################################################
def _setup_Executable_base_exte(base='Console', exte=''):
    if sys.platform == 'win32':
        base = 'Win32GUI'
        exte = '.exe'

    return(base, exte)

###############################################################################
def _keywords(keywords=[]):
    keywords.append(_language_name)
    return(' '.join(keywords))

###############################################################################
def _build_exe(path_base=None, project=None, version=None):
    build_exe = None

    if path_base is None:
        path_base = _build_exe_path_base

    if project and version:
        build_exe = os.path.join(os.path.join(*path_base)
                                ,_build_exe_name_seps.join([project, version])
                                ,_build_exe_path_init +
                                 _build_exe_name_seps.join([sys.platform
                                                           ,_build_exe_char_seps.join(platform.architecture())
                                                       #CZ#,platform.processor()
                                                       #CZ#,platform.machine()
                                                           ,_language_name
                                                           ,platform.python_version()
                                                           ])
                                )

    return(build_exe)

###############################################################################
def _get_version(version=None):
#CZ#if version is None:
#CZ#    from <ProjectName> import VERSION as version
#CZ#else:
    if version is not None:
        assert len(version) == 5
        assert version[3] in ('alpha', 'beta', 'rc', 'final')

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN    (for pre-alpha release)
    #     | {a|b|c}N (for alpha, beta and rc release)
    parts = 2 if version[2] == 0 else 3
    main ='.'.join(str(x) for x in version[:parts])

    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        vcs_changeset = _get_vcs_changeset()
        if vcs_changeset:
            sub = '.dev%s' % vcs_changeset

    elif version[3] != 'final':
        mapping = {'alpha':'a', 'beta':'b', 'rc':'c'}
        sub = mapping[version[3]] + str(version[4])

    return(str(main + sub))

###############################################################################
def _get_vcs_changeset(vcs_cmd=None):
    repoDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if vcs_cmd is None:
        vcs_cmd = 'git log --quiet -l 1 --pretty=format:%ct HEAD'
        vcs_cmd = 'svn log --quiet -1 1 -r HEAD'

    vcs_log = subprocess.Popen(vcs_cmd
                              ,stdout=subprocess.PIPE
                              ,stderr=subprocess.PIPE
                              ,shell=True
                              ,cwd=repoDir
                              ,universal_newlines=True
                              )
    timestamp = vcs_log.communicate()[0]

    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return(None)

    return(timestamp.strftime('%Y%m%d%H%M%S'))
