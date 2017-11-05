@echo off
call set-env-windows.bat
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

set name_prog=CurlUploader
set prog_main=CurlUploader\curl_uploader.py
set file_gear=images\gear.ico
set file_vers=setup-pyinstaller-version.txt

set verp_dist=.\dist\CurlUploader.exe
set verp_vers=0.1.0.0
set verp_desc=Simulate curl program for upload file.
set verp_prod=CurlUploader
set verp_copy=zappyk@gmail.com, 2017
set verp_comp=Carlo Zappacosta

set pyinstaller=pyinstaller.exe --clean --onefile --windowed --log-level=DEBUG
set pyinstaller=pyinstaller.exe --clean --onefile            --log-level=DEBUG

rem %pyinstaller% --icon %file_gear% --version-file %file_vers% --name %name_prog% %prog_main%
    %pyinstaller% --icon %file_gear%                            --name %name_prog% %prog_main%

set EXIT_CODE=%errorlevel%

if %EXIT_CODE% == 0 (
    echo _______________________________________________________________________________
    echo.
    verpatch.exe "%verp_dist%" %verp_vers% /va /pv %verp_vers% /s description "%verp_desc%" /s product "%verp_prod%" /s copyright "%verp_copy%" /s company "%verp_comp%"
    if %errorlevel% == 0 (
        echo    Assegnazione Versione/Patch eseguita con successo :D
    ) else (
        echo    Assegnazione Versione/Patch FALLITA, analizzare! o_O
    )
)

if %EXIT_CODE% == 0 (
    echo _______________________________________________________________________________
	echo.
	echo    COMPILAZINE RIUSCITA :D
	timeout /t 10 /nobreak
) else (
    echo _______________________________________________________________________________
	echo.
	echo    COMPILAZIONE NON RIUSCITA, CONTROLLARE L'ERRORE GENERATO...
	echo.
	pause
)

exit /b %EXIT_CODE%
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
rem General Options
rem
rem -h, --help	show this help message and exit
rem -v, --version	Show program version info and exit.
rem --distpath DIR	Where to put the bundled app (default: ./dist)
rem --workpath WORKPATH
rem  	Where to put all the temporary work files, .log, .pyz and etc. (default: ./build)
rem -y, --noconfirm
rem  	Replace output directory (default: SPECPATH/dist/SPECNAME) without asking for confirmation
rem --upx-dir UPX_DIR
rem  	Path to UPX utility (default: search the execution path)
rem -a, --ascii	Do not include unicode encoding support (default: included if available)
rem --clean	Clean PyInstaller cache and remove temporary files before building.
rem --log-level LEVEL
rem  	Amount of detail in build-time console messages. LEVEL may be one of DEBUG, INFO, WARN, ERROR, CRITICAL (default: INFO).
rem What to generate
rem
rem -D, --onedir	Create a one-folder bundle containing an executable (default)
rem -F, --onefile	Create a one-file bundled executable.
rem --specpath DIR	Folder to store the generated spec file (default: current directory)
rem -n NAME, --name NAME
rem  	Name to assign to the bundled app and spec file (default: first script's basename)
rem What to bundle, where to search
rem
rem -p DIR, --paths DIR
rem  	A path to search for imports (like using PYTHONPATH). Multiple paths are allowed, separated by ':', or use this option multiple times
rem --hidden-import MODULENAME, --hiddenimport MODULENAME
rem  	Name an import not visible in the code of the script(s). This option can be used multiple times.
rem --additional-hooks-dir HOOKSPATH
rem  	An additional path to search for hooks. This option can be used multiple times.
rem --runtime-hook RUNTIME_HOOKS
rem  	Path to a custom runtime hook file. A runtime hook is code that is bundled with the executable and is executed before any other code or module to set up special features of the runtime environment. This option can be used multiple times.
rem --exclude-module EXCLUDES
rem  	Optional module or package (his Python names, not path names) that will be ignored (as though it was not found). This option can be used multiple times.
rem --key KEY	The key used to encrypt Python bytecode.
rem How to generate
rem
rem -d, --debug	Tell the bootloader to issue progress messages while initializing and starting the bundled app. Used to diagnose problems with missing imports.
rem -s, --strip	Apply a symbol-table strip to the executable and shared libs (not recommended for Windows)
rem --noupx	Do not use UPX even if it is available (works differently between Windows and *nix)
rem Windows and Mac OS X specific options
rem
rem -c, --console, --nowindowed
rem  	Open a console window for standard i/o (default)
rem -w, --windowed, --noconsole
rem  	Windows and Mac OS X: do not provide a console window for standard i/o. On Mac OS X this also triggers building an OS X .app bundle. This option is ignored in *NIX systems.
rem -i <FILE.ico or FILE.exe,ID or FILE.icns>, --icon <FILE.ico or FILE.exe,ID or FILE.icns>
rem  	FILE.ico: applrem y that icon to a Windows executable. FILE.exe,ID, extract the icon with ID from an exe. FILE.icns: apply the icon to the .app bundle on Mac OS X
rem Windows specific options
rem
rem --version-file FILE
rem  	add a version resource from FILE to the exe
rem -m <FILE or XML>, --manifest <FILE or XML>
rem  	add manifest FILE rem or XML to the exe
rem -r RESOURCE, --resource RESOURCE
rem  	Add or update a resource to a Windows executable. The RESOURCE is one to four items, FILE[,TYPE[,NAME[,LANGUAGE]]]. FILE can be a data file or an exe/dll. For data files, at least TYPE and NAME must be specified. LANGUAGE defaults to 0 or may be specified as wildcard * to update all resources of the given TYPE and NAME. For exe/dll files, all resources from FILE will be added/updated to the final executable if TYPE, NAME and LANGUAGE are omitted or specified as wildcard *.This option can be used multiple times.
rem --uac-admin	Using this option creates a Manifest which will request elevation upon application restart.
rem --uac-uiaccess	Using this option allows an elevated application to work with Remote Desktop.
rem Windows Side-by-side Assembly searching options (advanced)
rem rem
rem --win-private-assemblies
rem  	Any Shared Assemblies bundled into the application will be changed into Private Assemblies. This means the exact versions of these assemblies will always be used, and any newer versions installed on user machines at the system level will be ignored.
rem --win-no-prefer-redirects
rem  	While searching for Shared or Private Assemblies to bundle into the application, PyInstaller will prefer not to follow policies that redirect to newer versions, and will try to bundle the exact versions of the assembly.
rem Mac OS X specific options
rem
rem --osx-bundle-identifier BUNDLE_IDENTIFIER
rem  	Mac OS X .app bundle identifier is used as the default unique program name for code signing purposes. The usual form is a hierarchical name in reverse DNS notation. For example: com.mycompany.department.appname (default: first script's basename)
rem Shortening the Command
