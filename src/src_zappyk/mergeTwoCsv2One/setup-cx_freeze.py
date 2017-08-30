import os
###############################################################################
project = 'MergeTwoCsv2One'
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

if os.name == 'nt':
    name = '%s.exe' % name

executables = [
    Executable(os.path.join(name, 'main.py'), base=base, targetName=name)
]

setup(name=name,
      version=version,
      description='Merge 2 file CSV in one file depending a columns keys',
      options=dict(build_exe = buildOptions),
      executables=executables)
