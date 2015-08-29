from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable('GoogleSheets/main.py', base=base, targetName = 'GoogleSheets')
]

setup(name='GoogleSheets',
      version = '1.0',
      description = 'Google Spreadsheet Read/Write to CSV',
      options = dict(build_exe = buildOptions),
      executables = executables)
