import os
project = 'GoogleSheets'
version = '1.0'

###############################################################################

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable(os.path.join(project, 'main.py'), base=base, targetName=project)
]

setup(name=project,
      version=version,
      description='Google Spreadsheet Read/Write (more?) manipulation',
      options=dict(build_exe = buildOptions),
      executables=executables)
