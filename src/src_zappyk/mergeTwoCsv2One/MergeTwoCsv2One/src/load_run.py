# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import csv
#CZ#import xlsxwriter

from tkinter            import *
from tkinter            import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showerror
from collections        import defaultdict

from lib_zappyk          import _initializeVariable
from lib_zappyk._os_file import _basenameNotExt, _basenameGetExt, _basenameFullPathNotExt, _fileExist
from lib_zappyk._string  import _trim, _trimList, _remove, _search, _findall, _joinSpace, _joinChar, _stringToList, _stringToListOnSpace

from MergeTwoCsv2One.cfg.load_cfg    import parser_args, parser_conf, logger_conf
from MergeTwoCsv2One.cfg.load_ini    import *
from MergeTwoCsv2One.src.constants   import *

args = parser_args().args
conf = parser_conf().conf
logs = logger_conf().logs

try:
    csv_delimiter      = conf.get("InputOutput", "csv_delimiter"     , fallback=csv_delimiter)
    csv_quotechar      = conf.get("InputOutput", "csv_quotechar"     , fallback=csv_quotechar)
    csv_quoting        = conf.get("InputOutput", "csv_quoting"       , fallback=csv_quoting)
    csv_lineterminator = conf.get("InputOutput", "csv_lineterminator", fallback=csv_lineterminator)
    key_columns_merge  = conf.get("KeyColMerge", "key_columns_merge" , fallback=key_columns_merge)
except:
    pass

csv_delimiter      = args.csv_delimiter      if args.csv_delimiter      is not None else csv_delimiter
csv_quotechar      = args.csv_quotechar      if args.csv_quotechar      is not None else csv_quotechar
csv_lineterminator = args.csv_lineterminator if args.csv_lineterminator is not None else csv_lineterminator
key_columns_merge  = args.key_columns_merge  if args.key_columns_merge  is not None else key_columns_merge

run_gui            = args.run_gui
run_cmd            = args.run_cmd
type_input         = args.type_input
file_input_master  = args.file_input_master
file_input_addcsv  = args.file_input_addcsv
file_output        = args.file_output
type_output        = args.type_output

run_gui            = True  if sys.platform == 'win32' else run_gui
run_gui            = False if run_cmd                 else run_gui

name_input_master  = _basenameNotExt(file_input_master)
name_input_addcsv  = _basenameNotExt(file_input_addcsv)
exte_output        = _basenameGetExt(file_output)
type_output        = TYPE_OUT_csv      if (type_output is None)           and (exte_output[1:] == TYPE_OUT_csv) else type_output
#CZ#type_output        = TYPE_OUT_xls      if (type_output is None)           and (exte_output[1:] == TYPE_OUT_xls) else type_output

file_output_csv    = '.'.join([_basenameFullPathNotExt(file_input_master), TYPE_OUT_csv])
#CZ#file_output_xls    = '.'.join([_basenameFullPathNotExt(file_input_master), TYPE_OUT_xls])

file_output        = file_output_csv   if (file_output is None)           and (type_output     == TYPE_OUT_csv) else file_output
#CZ#file_output        = file_output_xls   if (file_output is None)           and (type_output     == TYPE_OUT_xls) else file_output
file_output        = file_output_csv   if (file_output == CHAR_STD_INOUT) and (type_output     == TYPE_OUT_csv) else file_output
#CZ#file_output        = file_output_xls   if (file_output == CHAR_STD_INOUT) and (type_output     == TYPE_OUT_xls) else file_output

#csv_delimiter     = ','               if csv_delimiter      is None else csv_delimiter
#csv_quotechar     = '"'               if csv_quotechar      is None else csv_quotechar
#csv_quoting       = csv.QUOTE_MINIMAL if csv_quoting        is None else csv_quoting
csv_quoting        = csv.QUOTE_NONE    if csv_quoting        is None else csv_quoting
#csv_lineterminator= "\r\n"            if csv_lineterminator is None else csv_lineterminator
#key_columns_merge = ''                if key_columns_merge  is None else key_columns_merge

root                  = Tk()
root_path_file_master = StringVar()
root_path_file_addcsv = StringVar()
root_choose_in        = StringVar()
root_chooseext        = StringVar()
root_combo_out        = [('Merge file master with file month', TYPE_IN_mmam)
                        ,('...another report layout...'      , 'xxxx')]
root_filetypes        = (('Text files', '*.csv')
                        ,('All files' , '*.*'  ))

self__execute__entry   = _initializeVariable()

self_type_input        = _initializeVariable(); self_type_input       .set(type_input)
self_file_input_master = _initializeVariable(); self_file_input_master.set(file_input_master)
self_file_input_addcsv = _initializeVariable(); self_file_input_addcsv.set(file_input_addcsv)
self_name_input_master = _initializeVariable(); self_name_input_master.set(name_input_master)
self_name_input_addcsv = _initializeVariable(); self_name_input_addcsv.set(name_input_addcsv)
self_file_output       = _initializeVariable(); self_file_output      .set(file_output)
self_type_output       = _initializeVariable(); self_type_output      .set(type_output)

if file_input_master == file_output != CHAR_STD_INOUT:
    logs.error("File input '%s' can't be the same file output!" % file_input_master)

if args.debug >= 1:
    logs.info('run_gui            = %s' % repr(run_gui))
    logs.info('run_cmd            = %s' % repr(run_cmd))
    logs.info('type_input         = %s' % repr(type_input))
    logs.info('file_input_master  = %s' % repr(file_input_master))
    logs.info('file_input_addcsv  = %s' % repr(file_input_addcsv))
    logs.info('file_output        = %s' % repr(file_output))
    logs.info('type_output        = %s' % repr(type_output))
    logs.info('csv_delimiter      = %s' % repr(csv_delimiter))
    logs.info('csv_quotechar      = %s' % repr(csv_quotechar))
    logs.info('csv_lineterminator = %s' % repr(csv_lineterminator))
    logs.info('key_columns_merge  = %s' % repr(key_columns_merge))
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
def _root_load_file_master():
    filename = askopenfilename(filetypes=root_filetypes)
    if filename:
        try:
            print("*** qui *** ((%s))" % filename)
            root_path_file_master.set(filename)
        except:
            logs_error('Failed to read file\n%s' % filename, 'Open Source File')
        return

###############################################################################
def _root_load_file_addcsv():
    filename = askopenfilename(filetypes=root_filetypes)
    if filename:
        try:
            root_path_file_addcsv.set(filename)
        except:
            logs_error('Failed to read file\n%s' % filename, 'Open Source File')
        return


###############################################################################
def _root__execute_():
    file_input_master = root_path_file_master.get()
    file_input_addcsv = root_path_file_addcsv.get()
    type_input        = root_choose_in.get()
    type_output       = root_chooseext.get()

    name_input_master = _basenameNotExt(file_input_master)
    name_input_addcsv = _basenameNotExt(file_input_addcsv)
    name_output       = _basenameFullPathNotExt(file_input_master)
    name_output       = ''.join([name_output, '+merged+', name_input_addcsv])
#CZ#file_output_csv   = '.'.join([name_output, TYPE_OUT_csv]) if name_input != '' else CHAR_STD_INOUT
#CZ#file_output_xls   = '.'.join([name_output, TYPE_OUT_xls]) if name_input != '' else CHAR_STD_INOUT
    file_output_csv   = '.'.join([name_output, TYPE_OUT_csv]) if name_input_master != '' else CHAR_STD_INOUT
#CZ#file_output       = None
    file_output       = None              if (args.file_output == CHAR_STD_INOUT) else args.file_output
    file_output       = file_output_csv   if (file_output is None) and (type_output == TYPE_OUT_csv) else file_output
#CZ#file_output       = file_output_xls   if (file_output is None) and (type_output == TYPE_OUT_xls) else file_output

    type_input        = _root_combo_get(root_combo_out, type_input)

    self_type_input       .set(type_input)
    self_file_input_master.set(file_input_master)
    self_file_input_addcsv.set(file_input_addcsv)
    self_name_input_master.set(name_input_master)
    self_name_input_addcsv.set(name_input_addcsv)
    self_file_output      .set(file_output)
    self_type_output      .set(type_output)

    if _trim(name_input_master) == '':
        logs_info('Choose csv file Master, please!')
        return

    if _trim(name_input_addcsv) == '':
        logs_info('Choose csv file AddCSV, please!')
        return

    if not _fileExist(file_input_master):
        logs_info("File Master '%s' not exist!" % file_input_master)
        return

    if not _fileExist(file_input_addcsv):
        logs_info("File AddCSV '%s' not exist!" % file_input_addcsv)
        return

    manipulate()

###############################################################################
def _root__execute__entry_on_change(a, b, c):
    if root_path_file_master.get() == '':
        self__execute__entry.get().config(state=DISABLED)
    else:
        self__execute__entry.get().config(state=NORMAL)

    if root_path_file_addcsv.get() == '':
        self__execute__entry.get().config(state=DISABLED)
    else:
        self__execute__entry.get().config(state=NORMAL)

###############################################################################
def _root_destroy():
    root.destroy()
    sys.exit(0)

###############################################################################
def main_gui():
#CZ#from MergeTwoCsv2One.src.version     import the_version
#CZ#root.title(''Merge 2 file CSV in one file (ver. %s)' % the_version())
    from MergeTwoCsv2One import VERSION as version
    root.title('Merge 2 file CSV in one file (ver. %s)' % version)
    root.resizable(0,0)
    root.bind('<Return>', _root_load_file_master)
    root.bind('<Return>', _root_load_file_addcsv)

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
    style.map('root__execute__entry.TButton', foreground=[('pressed', 'green'), ('active', 'green')]
                                            , background=[('pressed', '!disabled', 'black'), ('active', 'white')]
    )
    style.map('root_cancel_entry.TButton', foreground=[('pressed', 'red'), ('active', 'red')]
                                         , background=[('pressed', '!disabled', 'black'), ('active', 'white')]
    )

    root_path_file_master_entry = ttk.Entry(mainframe, width=len_with_EC, textvariable=root_path_file_master)
    root_path_file_master_entry.focus()
    root_path_file_master.trace('w', _root__execute__entry_on_change) # rwua

    root_path_file_addcsv_entry = ttk.Entry(mainframe, width=len_with_EC, textvariable=root_path_file_addcsv)
    root_path_file_addcsv_entry.focus()
    root_path_file_addcsv.trace('w', _root__execute__entry_on_change)  # rwua

    root_choose_in_entry = ttk.Combobox(mainframe, width=len_with_EC, textvariable=root_choose_in, state='readonly')
    root_choose_in_entry['values'] = _root_combo_set(root_combo_out)
    root_choose_in_entry.current(0)

#CZ#root_choosecsv_entry = ttk.Radiobutton(mainframe, text='output in %s' % TYPE_OUT_csv.upper(), value=TYPE_OUT_csv, variable=root_chooseext)
#CZ#root_choosexls_entry = ttk.Radiobutton(mainframe, text='output in %s' % TYPE_OUT_xls.upper(), value=TYPE_OUT_xls, variable=root_chooseext)
#CZ#root_chooseext.set(TYPE_OUT_xls)
    root_chooseext.set(TYPE_OUT_csv)

#CZ#root_fsbrowser_entry = ttk.Button(mainframe, text='filesystem browser', width=len_with_B1, command=_root_load_file)
    root_fb_master_entry = ttk.Button(mainframe, text='filesystem browser', width=len_with_B1, command=_root_load_file_master)
    root_fb_addcsv_entry = ttk.Button(mainframe, text='filesystem browser', width=len_with_B1, command=_root_load_file_addcsv)
    root__execute__entry = ttk.Button(mainframe, text='Merge File', width=len_with_B2, command=_root__execute_, state=DISABLED, style='root__execute__entry.TButton')
    self__execute__entry.set(root__execute__entry)

    root_cancel_entry = ttk.Button(mainframe, text='CANCEL', width=len_with_B1, command=_root_destroy , style='root_cancel_entry.TButton')

    mainframe                                             .grid(column=0, row=0, sticky=(N, W, E, S))
    ttk.Label (mainframe, text="Choose CSV file through:").grid(column=1, row=1 , sticky=W)

    ttk.Label (mainframe, text=" · file CSV MASTER")      .grid(column=1, row=2 , sticky=W)
    root_fb_master_entry                                  .grid(column=2, row=2 , sticky=W)
    ttk.Label (mainframe, text="or enter")                .grid(column=3, row=2 , sticky=W)
    root_path_file_master_entry                           .grid(column=4, row=2 , sticky=(W, E))


    ttk.Label(mainframe, text=" · file CSV Add.Month")    .grid(column=1, row=3, sticky=W)
    root_fb_addcsv_entry                                  .grid(column=2, row=3, sticky=W)
    ttk.Label(mainframe, text="or enter")                 .grid(column=3, row=3, sticky=W)
    root_path_file_addcsv_entry                           .grid(column=4, row=3, sticky=(W, E))

    root_choose_in_entry                                  .grid(column=4, row=6 , sticky=(W, E))
    ttk.Label (mainframe, text="Choose type report text:").grid(column=1, row=6 , sticky=W)
#CZ#root_choosecsv_entry                                  .grid(column=4, row=7 , sticky=(W, E))
#CZ#root_choosexls_entry                                  .grid(column=4, row=8 , sticky=(W, E))
    root__execute__entry                                  .grid(column=4, row=9 , sticky=W)
    root_cancel_entry                                     .grid(column=4, row=11, sticky=E)

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
        logs.info('type_input        = %s' % self_type_input.get())
        logs.info('file_input_master = %s' % self_file_input_master.get())
        logs.info('file_input_addcsv = %s' % self_file_input_addcsv.get())
        logs.info('file_output       = %s' % self_file_output.get())
        logs.info('type_output       = %s' % self_type_output.get())
        logs.info('-------------------')

    try:
        csv_lines_master = read_filein_master()
        csv_lines_addcsv = read_filein_addcsv()

        dat_lines = None
       #if type_input ==  TYPE_IN_mmam:
        if self_type_input.get() ==  TYPE_IN_mmam:
            dat_lines = manipulate_mmam(csv_lines_master, csv_lines_addcsv)
        else:
           #logs_error("Type input '%s' can't be configurate!" % type_input)
            logs_error("Type input '%s' can't be configurate!" % self_type_input.get())

        write_fileout(dat_lines)

       #logs_info('Merge CSV completed!\n\nOpen file output on:\n%s' % file_output)
        logs_info('Merge CSV completed!\n\nOpen file output on:\n%s' % self_file_output.get())

    except ValueError:
        pass

###############################################################################
def manipulate_mmam(csv_lines_master, csv_lines_addcsv):
    keys = _stringToList(key_columns_merge, CHAR_KEY_SPLIT)
#CZ#keys = [map(lambda value: value.upper(), keys)]
    keys = [value.upper() for value in keys]
    kadd = {}
    #__________________________________________________________________________
    #
    Ckeys = []
    Vkeys = []
    first = True
    count_row = 0
    count_col = 0
    lines_add = {}
    #==========================================================================
    for csv_line_addcsv in csv_lines_addcsv:
        count_row = count_row +1

        if first:
            first = False
            count_col = 0
            for value in csv_line_addcsv:
                count_col = count_col +1
                finds = [key for key in keys if key == value.upper()]
                if len(finds) > 0:
                    Ckeys.append(count_col-1)
                if args.debug >= 3:
                    logs_info("AddCSV line %3s.%2s [%s]" % (count_row, count_col, value))
            if args.debug >= 2:
                logs_info('AddCSV:')

        else:
            if args.debug >= 3:
                logs_info("AddCSV line %3s.   [%s]" % (count_row, csv_line_addcsv))

            Vkeys = []
            for k in Ckeys:
                Vkeys.append(csv_line_addcsv[Ckeys[k]])
            Skeys = _joinChar(Vkeys, CHAR_KEY_SPLIT)
            debug = 'read'

            lines_row = [csv_line_addcsv]
            if Skeys in lines_add:
                lines_row = lines_add[Skeys]
                lines_row.append(csv_line_addcsv)
            lines_add[Skeys] = lines_row

            if args.debug >= 2:
                logs_info('AddCSV %-5s (%s) == (%s)' % (debug, Skeys, csv_line_addcsv))

    #__________________________________________________________________________
    #
    Ckeys = []
    Vkeys = []
    first = True
    count_row = 0
    count_col = 0
    lines_out = []
    #==========================================================================
    for csv_line_master in csv_lines_master:
        count_row = count_row +1

        if first:
            first = False
            count_col = 0
            for value in csv_line_master:
                count_col = count_col +1
                finds = [key for key in keys if key == value.upper()]
                if len(finds) > 0:
                    Ckeys.append(count_col-1)
                if args.debug >= 3:
                    logs_info("Master line %3s.%2s [%s]" % (count_row, count_col, value))
            if args.debug >= 2:
                 logs_info('Master:')

            lines_out.append(csv_line_master)
        else:
            if args.debug >= 3:
                logs_info("Master line %3s.   [%s]" % (count_row, csv_line_master))

            Vkeys = []
            for k in Ckeys:
                Vkeys.append(csv_line_master[Ckeys[k]])
            Skeys = _joinChar(Vkeys, CHAR_KEY_SPLIT)
            debug = ''

            if Skeys in lines_add:
                if Skeys in kadd:
                    debug = 'SKIP!'
                else:
                    debug = 'REPL.'
                    for key, row in lines_add.items():
                        if key == Skeys:
                            for line in row:
                                lines_out.append(line)
                                if args.debug >= 2:
                                    logs_info('Master %-5s (%s) == (%s)' % (debug, Skeys, line))
                    kadd[Skeys] = True
                    del(lines_add[Skeys])
            else:
                if Skeys in kadd:
                    debug = 'SKIP!'
                else:
                    debug = 'write'
                    lines_out.append(csv_line_master)

            if args.debug >= 2:
                logs_info('Master %-5s (%s) == (%s)' % (debug, Skeys, csv_line_master))

    for key, row in lines_add.items():
        for line in row:
            lines_out.append(line)

    if args.debug >= 1:
        logs.info('out values=')
        logs_info(_joinChar(str(values) for values in lines_out))

    return(lines_out)

###############################################################################
def read_filein(file_csv):
   #csv_filename = file_input_master
   #csv_filename = self_file_input_master.get()
    csv_filename = file_csv

    filein = None
    std_in = False
    if csv_filename == CHAR_STD_INOUT:
        filein = sys.stdin
        std_in = True
        logs.info('Read csv rows on STDIN:')
    else:
        if not _fileExist(csv_filename):
            logs_error("Can't read file '%s', exist?" % csv_filename)
        try:
            filein = open(csv_filename, 'r')
            logs.info('Read on file csv: %s' % csv_filename)
        except:
            filein = sys.stdin
            std_in = True
            logs.info('File csv not set, read on STDIN:')

    if std_in:
        logs.info(LINE_PARTITION)

#CZ#txt_lines = filein.readlines()
    csv_lines = list(csv.reader(filein, delimiter=csv_delimiter))
    if std_in:
        logs.info(LINE_PARTITION)

    if args.debug >= 3:
        logs.info('csv values=')
#CZ#    for values in txt_lines:
#CZ#        logs.info(values)
       #logs_info('\n'.join(str(values) for values in csv_lines))
        logs_info(_joinChar(str(values) for values in csv_lines))

#CZ#return(txt_lines)
    return(csv_lines)

###############################################################################
def read_filein_master():
    return(read_filein(self_file_input_master.get()))

###############################################################################
def read_filein_addcsv():
    return(read_filein(self_file_input_addcsv.get()))

###############################################################################
def write_fileout(dat_lines):
   #txt_filename = file_input_master
   #out_filename = file_output
    txt_filename = self_file_input_master.get()
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

#CZ#name_ws = None
#CZ#if txt_filename != CHAR_STD_INOUT:
#CZ#   #name_ws = name_input_master
#CZ#    name_ws = self_name_input_master.get()

    if std_out:
        logs.info(LINE_PARTITION)
    if typeout == TYPE_OUT_csv:
        write_filecsv(dat_lines, fileout)
#CZ#if typeout == TYPE_OUT_xls:
#CZ#    write_filexls(dat_lines, name_ws)
    if std_out:
        logs.info(LINE_PARTITION)

###############################################################################
def write_filecsv(dat_lines, fileout):
   #csv_values= csv.writer(fileout)
    csv_values = csv.writer(fileout, delimiter=csv_delimiter, quotechar=csv_quotechar, quoting=csv_quoting, lineterminator=csv_lineterminator)
    csv_values.writerows(dat_lines)

#CZ################################################################################
#CZ#def write_filexls(dat_lines, name_ws='Report'):
#CZ#   #out_filename = file_output
#CZ#    out_filename = self_file_output.get()
#CZ#
#CZ#    workbook = xlsxwriter.Workbook(out_filename)
#CZ#    worksheet = workbook.add_worksheet(name_ws)
#CZ#
#CZ#    format_head = workbook.add_format({'bold': True, 'italic': True, 'shrink': True, 'font_color': 'white', 'bg_color': 'black'})
#CZ#
#CZ#    row = 0
#CZ#    for dat_line in dat_lines:
#CZ#        col = 0
#CZ#        for value in dat_line:
#CZ#            if (col >= 2) and value.isdigit():
#CZ#                value = float(value)
#CZ#            if (row == 0):
#CZ#                worksheet.write(row, col, value, format_head)
#CZ#            else:
#CZ#                worksheet.write(row, col, value)
#CZ#            col += 1
#CZ#        row += 1
#CZ#
#CZ#    workbook.close()

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