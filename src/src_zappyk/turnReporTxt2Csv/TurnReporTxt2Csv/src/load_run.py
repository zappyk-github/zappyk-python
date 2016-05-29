# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import csv
import xlsxwriter

from tkinter            import *
from tkinter            import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showerror

from lib_zappyk          import _initializeVariable
from lib_zappyk._os_file import _basenameNotExt, _basenameGetExt, _basenameFullPathNotExt, _fileExist
from lib_zappyk._string  import _trim, _trimList, _remove, _search, _findall, _joinSpace, _stringToList, _stringToListOnSpace

from TurnReporTxt2Csv.cfg.load_cfg    import parser_args, parser_conf, logger_conf
from TurnReporTxt2Csv.cfg.load_ini    import *
from TurnReporTxt2Csv.src.constants   import *

args = parser_args().args
conf = parser_conf().conf
logs = logger_conf().logs

try:
    csv_delimiter      = conf.get("InputOutput", "csv_delimiter"     , fallback=csv_delimiter)
    csv_quotechar      = conf.get("InputOutput", "csv_quotechar"     , fallback=csv_quotechar)
    csv_quoting        = conf.get("InputOutput", "csv_quoting"       , fallback=csv_quoting)
    csv_lineterminator = conf.get("InputOutput", "csv_lineterminator", fallback=csv_lineterminator)
except:
    pass

csv_delimiter      = args.csv_delimiter      if args.csv_delimiter      is not None else csv_delimiter
csv_quotechar      = args.csv_quotechar      if args.csv_quotechar      is not None else csv_quotechar
csv_lineterminator = args.csv_lineterminator if args.csv_lineterminator is not None else csv_lineterminator

run_gui            = args.run_gui
run_cmd            = args.run_cmd
type_input         = args.type_input
file_input         = args.file_input
file_output        = args.file_output
type_output        = args.type_output

run_gui            = True  if sys.platform == 'win32' else run_gui
run_gui            = False if run_cmd                 else run_gui

name_input         = _basenameNotExt(file_input)
exte_output        = _basenameGetExt(file_output)
type_output        = TYPE_OUT_csv      if (type_output is None)           and (exte_output[1:] == TYPE_OUT_csv) else type_output
type_output        = TYPE_OUT_xls      if (type_output is None)           and (exte_output[1:] == TYPE_OUT_xls) else type_output

file_output_csv    = '.'.join([_basenameFullPathNotExt(file_input), TYPE_OUT_csv])
file_output_xls    = '.'.join([_basenameFullPathNotExt(file_input), TYPE_OUT_xls])

file_output        = file_output_csv   if (file_output is None)           and (type_output     == TYPE_OUT_csv) else file_output
file_output        = file_output_xls   if (file_output is None)           and (type_output     == TYPE_OUT_xls) else file_output
file_output        = file_output_csv   if (file_output == CHAR_STD_INOUT) and (type_output     == TYPE_OUT_csv) else file_output
file_output        = file_output_xls   if (file_output == CHAR_STD_INOUT) and (type_output     == TYPE_OUT_xls) else file_output

#csv_delimiter     = ','               if csv_delimiter      is None else csv_delimiter
#csv_quotechar     = '"'               if csv_quotechar      is None else csv_quotechar
#csv_quoting       = csv.QUOTE_MINIMAL if csv_quoting        is None else csv_quoting
csv_quoting        = csv.QUOTE_NONE    if csv_quoting        is None else csv_quoting
#csv_lineterminator= "\r\n"            if csv_lineterminator is None else csv_lineterminator

root           = Tk()
root_path_file = StringVar()
root_choose_in = StringVar()
root_chooseext = StringVar()
root_combo_out = [('Analisi delle Vendite su 8 Periodi', TYPE_IN_av8p)
                 ,('...another report layout...'       , 'xxxx')]
root_filetypes = (('Text files', '*.txt')
                 ,('All files' , '*.*'  ))

self_translate_entry = _initializeVariable()

self_type_input    = _initializeVariable(); self_type_input .set(type_input)
self_file_input    = _initializeVariable(); self_file_input .set(file_input)
self_name_input    = _initializeVariable(); self_name_input .set(name_input)
self_file_output   = _initializeVariable(); self_file_output.set(file_output)
self_type_output   = _initializeVariable(); self_type_output.set(type_output)

if file_input == file_output != CHAR_STD_INOUT:
    logs.error("File input '%s' can't be the same file output!" % file_input)

if args.debug >= 1:
    logs.info('run_gui            = %s' % repr(run_gui))
    logs.info('run_cmd            = %s' % repr(run_cmd))
    logs.info('type_input         = %s' % repr(type_input))
    logs.info('file_input         = %s' % repr(file_input))
    logs.info('file_output        = %s' % repr(file_output))
    logs.info('type_output        = %s' % repr(type_output))
    logs.info('csv_delimiter      = %s' % repr(csv_delimiter))
    logs.info('csv_quotechar      = %s' % repr(csv_quotechar))
    logs.info('csv_lineterminator = %s' % repr(csv_lineterminator))
    logs.info('--------------------')

###############################################################################
def _root_combo_set(root_combo_out):
    root_value_out = []
    for text, value in root_combo_out:
        root_value_out.append(text)
    return(root_value_out)

###############################################################################
def _root_combo_get(root_combo_out, type_input):
    for text, value in root_combo_out:
        if text == type_input:
            type_input = value
    return(type_input)

###############################################################################
def _root_load_file():
    filename = askopenfilename(filetypes=root_filetypes)
    if filename:
        try:
            root_path_file.set(filename)
        except:
            logs_error('Failed to read file\n%s' % filename, 'Open Source File')
        return

###############################################################################
def _root_translate():
    file_input       = root_path_file.get()
    type_input       = root_choose_in.get()
    type_output      = root_chooseext.get()

    name_input       = _basenameNotExt(file_input)
    name_output      = _basenameFullPathNotExt(file_input)
    file_output_csv  = '.'.join([name_output, TYPE_OUT_csv]) if name_input != '' else CHAR_STD_INOUT
    file_output_xls  = '.'.join([name_output, TYPE_OUT_xls]) if name_input != '' else CHAR_STD_INOUT
    file_output      = None
    file_output      = file_output_csv   if (file_output is None) and (type_output == TYPE_OUT_csv) else file_output
    file_output      = file_output_xls   if (file_output is None) and (type_output == TYPE_OUT_xls) else file_output

    type_input       = _root_combo_get(root_combo_out, type_input)

    self_type_input .set(type_input)
    self_file_input .set(file_input)
    self_name_input .set(name_input)
    self_file_output.set(file_output)
    self_type_output.set(type_output)

    if _trim(name_input) == '':
        logs_info('Choose text file report, please!')
        return

    if not _fileExist(file_input):
        logs_info("File report '%s' not exist!" % file_input)
        return

    manipulate()

###############################################################################
def _root_translate_entry_on_change(a, b, c):
    if root_path_file.get() == '':
        self_translate_entry.get().config(state=DISABLED)
    else:
        self_translate_entry.get().config(state=NORMAL)

###############################################################################
def _root_destroy():
    root.destroy()
    sys.exit(0)

###############################################################################
def main_gui():
#CZ#from TurnReporTxt2Csv.src.version     import the_version
#CZ#root.title('Manipulation Text Report (ver. %s)' % the_version())
    from TurnReporTxt2Csv import VERSION as version
    root.title('Manipulation Text Report (ver. %s)' % version)
    root.resizable(0,0)
    root.bind('<Return>', _root_load_file)

    mainframe = ttk.Frame(root, padding='3 3 12 12')
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    len_padding = 6
    len_font_MF = 12
    len_with_EC = 70
    len_with_B1 = 20
    len_with_B2 = 30

    style = ttk.Style()
    style.configure('.', padding=len_padding, relief='flat', font=('Helvetica', len_font_MF), foreground='black', background='#ccc')
    style.map('root_translate_entry.TButton', foreground=[('pressed', 'green'), ('active', 'green')]
                                            , background=[('pressed', '!disabled', 'black'), ('active', 'white')]
    )
    style.map('root_cancel_entry.TButton', foreground=[('pressed', 'red'), ('active', 'red')]
                                         , background=[('pressed', '!disabled', 'black'), ('active', 'white')]
    )

    root_path_file_entry = ttk.Entry(mainframe, width=len_with_EC, textvariable=root_path_file)
    root_path_file_entry.focus()
    root_path_file.trace('w', _root_translate_entry_on_change) # rwua

    root_choose_in_entry = ttk.Combobox(mainframe, width=len_with_EC, textvariable=root_choose_in, state='readonly')
    root_choose_in_entry['values'] = _root_combo_set(root_combo_out)
    root_choose_in_entry.current(0)

    root_choosecsv_entry = ttk.Radiobutton(mainframe, text='output in %s' % TYPE_OUT_csv.upper(), value=TYPE_OUT_csv, variable=root_chooseext)
    root_choosexls_entry = ttk.Radiobutton(mainframe, text='output in %s' % TYPE_OUT_xls.upper(), value=TYPE_OUT_xls, variable=root_chooseext)
    root_chooseext.set(TYPE_OUT_xls)

    root_fsbrowser_entry = ttk.Button(mainframe, text='filesystem browser', width=len_with_B1, command=_root_load_file)
    root_translate_entry = ttk.Button(mainframe, text='Translate', width=len_with_B2, command=_root_translate, state=DISABLED, style='root_translate_entry.TButton')
    self_translate_entry.set(root_translate_entry)

    root_cancel_entry = ttk.Button(mainframe, text='CANCEL', width=len_with_B1, command=_root_destroy , style='root_cancel_entry.TButton')

    mainframe                                              .grid(column=0, row=0, sticky=(N, W, E, S))
    ttk.Label (mainframe, text="Choose text file through:").grid(column=1, row=1, sticky=W)
    root_fsbrowser_entry                                   .grid(column=1, row=2, sticky=W)
    ttk.Label (mainframe, text="or enter")                 .grid(column=2, row=2, sticky=W)
    root_path_file_entry                                   .grid(column=3, row=2, sticky=(W, E))
    root_choose_in_entry                                   .grid(column=3, row=3, sticky=(W, E))
    ttk.Label (mainframe, text="Choose type report text:") .grid(column=1, row=3, sticky=W)
    root_choosecsv_entry                                   .grid(column=3, row=4, sticky=(W, E))
    root_choosexls_entry                                   .grid(column=3, row=5, sticky=(W, E))
    root_translate_entry                                   .grid(column=3, row=6, sticky=W)
    root_cancel_entry                                      .grid(column=3, row=8, sticky=E)

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    root.mainloop()

###############################################################################
def main():
    if run_gui:
        try:
            while True:
                main_gui()
        except Exception as e:
            print(str(e))
            sys.exit(1)
    else:
        manipulate()

    sys.exit(0)

###############################################################################
def manipulate():
    if args.debug >= 1:
        logs.info('type_input  = %s' % self_type_input.get())
        logs.info('file_input  = %s' % self_file_input.get())
        logs.info('file_output = %s' % self_file_output.get())
        logs.info('type_output = %s' % self_type_output.get())
        logs.info('-------------')

    try:
        txt_lines = read_filein()

        dat_lines = None
       #if type_input ==  TYPE_IN_av8p:
        if self_type_input.get() ==  TYPE_IN_av8p:
            dat_lines = manipulate_av8p(txt_lines)
        else:
           #logs_error("Type input '%s' can't be configurate!" % type_input)
            logs_error("Type input '%s' can't be configurate!" % self_type_input.get())

        write_fileout(dat_lines)

       #logs_info('Translate completed!\n\nOpen file output on:\n%s' % file_output)
        logs_info('Translate completed!\n\nOpen file output on:\n%s' % self_file_output.get())

    except ValueError:
        pass

###############################################################################
def manipulate_av8p(txt_lines):
    tmp_lines = []
    dat_lines = []

    dat_head_0 = True
    dat_body_1 = False
    dat_body_2 = False

    row_head_0 = None
    row_body_1 = None
    row_body_2 = None

    fld_first  = 45
    fld_code   = 10
    fld_name   = fld_first - fld_code
    frm_first  = '%'+str(fld_code)+'s' + csv_delimiter + '%-'+str(fld_name)+'s'

    reg_head_0 = 'DAL .* TOTALI'
    reg_body_1 = '\d{1,'+str(fld_code)+'}\s\s?\w'

   #rec_head_0 = re.compile(reg_head_0, re.I|re.L|re.M|re.U|re.S)
   #rec_body_1 = re.compile(reg_body_1, re.I|re.L|re.M|re.U|re.S)

    #__________________________________________________________________________
    for txt_line in txt_lines:
        txt_line = _remove(txt_line, "\f\r\n")
        txt_line = normalize_string(txt_line)

        if args.debug >= 2:
            print("#-|"+txt_line)
        #______________________________________________________________________
       #if dat_head_0 and rec_head_0.search(txt_line):
        if dat_head_0 and _search(reg_head_0, txt_line):
            dat_head_0 = False
            dat_body_1 = True

            row_head_0 = (frm_first % ('Codice', 'Prodotto')) + txt_line

            tmp_lines.append(row_head_0)
            if args.debug >= 1:
                print("#1#" + row_head_0)
        #______________________________________________________________________
        if dat_body_2:
            dat_body_1 = True
            dat_body_2 = False

            row_body_2 = row_body_1 + txt_line

            tmp_lines.append(row_body_2)
            if args.debug >= 1:
                print("#1|" + row_body_2)
        #______________________________________________________________________
       #if dat_body_1 and rec_body_1.search(txt_line) and len(txt_line)<=fld_first:
        if dat_body_1 and _search(reg_body_1, txt_line) and len(txt_line)<=fld_first:
            dat_body_1 = False
            dat_body_2 = True

            list = _stringToListOnSpace(_trim(txt_line))

            code = list[0]                     if len(list) > 0 else None
            name = _trim(_joinSpace(list[1:])) if len(list) > 1 else None

            row_body_1 = frm_first % (code, name)

    #__________________________________________________________________________
    for txt_line in tmp_lines:
        txt_line = string_to_csv(txt_line, csv_delimiter, fld_first, 6, 14)
        if args.debug >= 1:
            print("#2|" + txt_line)
        cvs_line = _stringToList(txt_line, csv_delimiter)
        cvs_line = _trimList(cvs_line)
        dat_lines.append(cvs_line)
    return(dat_lines)

###############################################################################
def normalize_string(string_old):
    string_new = string_old
    re_compile = re.compile("^(.*)\s(\d{1,3}),(\d.*)$")
    while _search(re_compile, string_new):
        findall = _findall(re_compile, string_new)
        if len(findall) > 0:
            string_new = '%s  %s%s' % findall[0]
    return(string_new)

###############################################################################
def string_to_csv(string, csv_delimiter, fld_first, length, step):
    r = csv_delimiter
    f = fld_first
    l = length
    s = step
    i = f+l; string = string[:i]+r+string[i:] if len(string) > i else string; l+=s+len(r) # col. 1
    i = f+l; string = string[:i]+r+string[i:] if len(string) > i else string; l+=s+len(r) # col. 2
    i = f+l; string = string[:i]+r+string[i:] if len(string) > i else string; l+=s+len(r) # col. 3
    i = f+l; string = string[:i]+r+string[i:] if len(string) > i else string; l+=s+len(r) # col. 4
    i = f+l; string = string[:i]+r+string[i:] if len(string) > i else string; l+=s+len(r) # col. 5
    i = f+l; string = string[:i]+r+string[i:] if len(string) > i else string; l+=s+len(r) # col. 6
    i = f+l; string = string[:i]+r+string[i:] if len(string) > i else string; l+=s+len(r) # col. 7
    i = f+l; string = string[:i]+r+string[i:] if len(string) > i else string; l+=s+len(r) # col. 8
    i = f+l; string = string[:i]+r+string[i:] if len(string) > i else string; l+=s+len(r) # col. 9
    return(string)

###############################################################################
def read_filein():
   #txt_filename = file_input
    txt_filename = self_file_input.get()

    filein = None
    std_in = False
    if txt_filename == CHAR_STD_INOUT:
        filein = sys.stdin
        std_in = True
        logs.info('Read txt rows on STDIN:')
    else:
        if not _fileExist(txt_filename):
            logs_error("Can't read file '%s', exist?" % txt_filename)
        try:
            filein = open(txt_filename, 'r')
            logs.info('Read on file txt: %s' % txt_filename)
        except:
            filein = sys.stdin
            std_in = True
            logs.info('File txt not set, read on STDIN:')

    if std_in:
        logs.info(LINE_PARTITION)
   #csv_lines = list(csv.reader(filein, delimiter=csv_delimiter))
    txt_lines = filein.readlines()
    if std_in:
        logs.info(LINE_PARTITION)

    if args.debug >= 3:
        logs.info('txt values=')
        for values in txt_lines:
            logs.info(values)

    return(txt_lines)

###############################################################################
def write_fileout(dat_lines):
   #txt_filename = file_input
   #out_filename = file_output
    txt_filename = self_file_input.get()
    out_filename = self_file_output.get()

    fileout = None
    std_out = False
   #typeout = type_output
    typeout = self_type_output.get()
    if out_filename == CHAR_STD_INOUT:
        fileout = sys.stdout
        typeout = TYPE_OUT_csv
        std_out = True
        logs.info('Write %s rows on STDOUT:' % typeout)
    else:
        try:
            fileout = open(out_filename, 'w')
            logs.info('Write to file out %s: %s' % (typeout, out_filename))
        except:
            fileout = sys.stdout
            std_out = True
            logs.info('File out not set, write on STDOUT:')

    name_ws = None
    if txt_filename != CHAR_STD_INOUT:
       #name_ws = name_input
        name_ws = self_name_input.get()

    if std_out:
        logs.info(LINE_PARTITION)
    if typeout == TYPE_OUT_csv:
        write_filecsv(dat_lines, fileout)
    if typeout == TYPE_OUT_xls:
        write_filexls(dat_lines, name_ws)
    if std_out:
        logs.info(LINE_PARTITION)

###############################################################################
def write_filecsv(dat_lines, fileout):
   #csv_values= csv.writer(fileout)
    csv_values = csv.writer(fileout, delimiter=csv_delimiter, quotechar=csv_quotechar, quoting=csv_quoting, lineterminator=csv_lineterminator)
    csv_values.writerows(dat_lines)

###############################################################################
def write_filexls(dat_lines, name_ws='Report'):
   #out_filename = file_output
    out_filename = self_file_output.get()

    workbook = xlsxwriter.Workbook(out_filename)
    worksheet = workbook.add_worksheet(name_ws)

    format_head = workbook.add_format({'bold': True, 'italic': True, 'shrink': True, 'font_color': 'white', 'bg_color': 'black'})

    row = 0
    for dat_line in dat_lines:
        col = 0
        for value in dat_line:
            if (col >= 2) and value.isdigit():
                value = float(value)
            if (row == 0):
                worksheet.write(row, col, value, format_head)
            else:
                worksheet.write(row, col, value)
            col += 1
        row += 1

    workbook.close()

###############################################################################
def logs_info(message, title='Info'):
    logs.info(message)
    if run_gui:
        showinfo(title, message)

###############################################################################
def logs_error(message, title='Error'):
    logs.error(message)
    if run_gui:
        showerror(title, message)

###############################################################################
def make_question(rows):
    line = rows[0]
    rive = '_' * len(line)
    rows.insert(0, rive)
    text = "\n".join(rows)
    return(text)

###############################################################################
def wait(seconds):
    import time
    time.sleep(seconds)

###############################################################################
def open_file(file):
#CZ#return(open(file))
#CZ#return(open(file, 'r', encoding="ascii"     , errors="surrogateescape"))
#CZ#return(open(file, 'r', encoding="ascii"     , errors="replace"))
#CZ#return(open(file, 'r', encoding="utf-8"     , errors="replace"))
    return(open(file, 'r', encoding="iso-8859-1", errors="replace"))