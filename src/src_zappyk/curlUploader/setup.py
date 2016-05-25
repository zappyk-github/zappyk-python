#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os, sys

from lib_zappyk import _setup

from CurlUploader.check_disk_space import _project, _description, _version

#CZ#project = 'CurlUploader'

#CZ#name         = __import__(project).get_project()
#CZ#description  = __import__(project).get_description()
#CZ#version      = __import__(project).get_version()
name         = _project
description  = _description
version      = _version
author       = _setup.AUTHOR
author_email = _setup.AUTHOR_EMAIL
license      = _setup.LICENSE
url          = _setup.URL
keywords     = _setup._keywords([author])

path_execute = [name]
name_execute = 'check_disk_space.py'

path_img_ico = ['images']
name_img_ico = 'gear.ico'

file_execute = os.path.join(os.path.join(*path_execute), name_execute)
file_img_ico = os.path.join(os.path.join(*path_img_ico), name_img_ico)

pkgs_exclude = ['tkinter', 'PyQt4']
#pkgs_include= _setup._find_packages('.', pkgs_exclude)
pkgs_include = _setup._find_packages(exclude=pkgs_exclude)
#file_include = ['%s-launch.bat' % project]
file_include = ['%s-launch.bat' % _project]

build_exe    = None
build_exe    = _setup._build_exe(None, name, version)

###############################################################################
(base, exte) = _setup._setup_Executable_base_exte()

executables = _setup._setup_Executable(file_execute
                        ,base=base
                        ,icon=file_img_ico
                        ,appendScriptToExe=False
                        ,appendScriptToLibrary=False
                        ,copyDependentFiles=True
                        ,targetName=name+exte
                        )
'''
options = {
    'build_exe': {
        'create_shared_zip': False,
        'compressed': True,
        'packages': pkgs_include,
        'excludes': pkgs_exclude,
        'include_files': file_include,
        'includes': [
            'testfreeze_1',
            'testfreeze_2'
        ],
        'path': sys.path + ['modules']
    }
}
'''

buildOptions = dict(create_shared_zip=False
                   ,compressed=True
                   ,packages=pkgs_include
                   ,excludes=pkgs_exclude
                   ,include_files=file_include
               #   ,namespace_packages=[name]
               #   ,path=sys.path+['/path/more/modules']
                   ,build_exe=build_exe
                   )

setupOptions = dict(name=name
                   ,version=version
                   ,url=url
                   ,author=author
                   ,author_email=author_email
                   ,description=description
                   ,license=license
                   ,keywords=keywords
                   ,executables=[executables]
                   ,options=dict(build_exe=buildOptions)
               #   ,packages=pkgs_include
               #   ,include_package_data=True
               #   ,scripts=[file_execute]
               #   ,zip_safe=True
                   )

_setup._setup(**setupOptions)
###############################################################################

sys.exit(0)
