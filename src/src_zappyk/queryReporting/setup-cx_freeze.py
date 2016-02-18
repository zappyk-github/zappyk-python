import os
###############################################################################
project = 'QueryReporting'
#
name         = __import__(project).get_project()
description  = __import__(project).get_description()
version      = __import__(project).get_version()
###############################################################################

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'
base = 'Win32GUI'

executables = [
    Executable(os.path.join(name, 'main.py'), base=base, targetName=name)
]

setup(name=name,
      version=version,
      description='Query Reporting management with output CSV/XLS file',
      options=dict(build_exe = buildOptions),
      executables=executables)
