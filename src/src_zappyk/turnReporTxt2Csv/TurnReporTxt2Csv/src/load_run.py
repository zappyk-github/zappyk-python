# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import re
import sys
import csv
import xlsxwriter

from tkinter import *
from tkinter import ttk

from lib_zappyk._os_file import _basenameNotExt, _basenameGetExt, _basenameFullPathNotExt, _fileExist
from lib_zappyk._string  import _trim, _trimList, _remove, _search, _findall, _joinSpace, _stringToList, _stringToListOnSpace

from TurnReporTxt2Csv.cfg.load_cfg  import parser_args, parser_conf, logger_conf
from TurnReporTxt2Csv.cfg.load_ini  import *
from TurnReporTxt2Csv.src.constants import *

args = parser_args().args
conf = parser_conf().conf
logs = logger_conf().logs

csv_delimiter      = conf.get("InputOutput", "csv_delimiter"     , fallback=csv_delimiter)
csv_quotechar      = conf.get("InputOutput", "csv_quotechar"     , fallback=csv_quotechar)
csv_quoting        = conf.get("InputOutput", "csv_quoting"       , fallback=csv_quoting)
csv_lineterminator = conf.get("InputOutput", "csv_lineterminator", fallback=csv_lineterminator)

csv_delimiter      = args.csv_delimiter      if args.csv_delimiter      is not None else csv_delimiter
csv_quotechar      = args.csv_quotechar      if args.csv_quotechar      is not None else csv_quotechar
csv_lineterminator = args.csv_lineterminator if args.csv_lineterminator is not None else csv_lineterminator

run_gui            = args.run_gui
type_input         = args.type_input
file_input         = args.file_input
file_output        = args.file_output
type_output        = args.type_output

name_output        = _basenameNotExt(file_output)
exte_output        = _basenameGetExt(file_output)
type_output        = TYPE_OUT_csv      if (type_output is None)           and (exte_output[1:] == TYPE_OUT_csv) else type_output
type_output        = TYPE_OUT_xls      if (type_output is None)           and (exte_output[1:] == TYPE_OUT_xls) else type_output

file_output_csv    = _basenameFullPathNotExt(file_input)+'.'+TYPE_OUT_csv
file_output_xls    = _basenameFullPathNotExt(file_input)+'.'+TYPE_OUT_xls
file_output        = file_output_csv   if (file_output is None)           and (type_output     == TYPE_OUT_csv) else file_output
file_output        = file_output_xls   if (file_output is None)           and (type_output     == TYPE_OUT_xls) else file_output
file_output        = file_output_csv   if (file_output == CHAR_STD_INOUT) and (type_output     == TYPE_OUT_csv) else file_output
file_output        = file_output_xls   if (file_output == CHAR_STD_INOUT) and (type_output     == TYPE_OUT_xls) else file_output

#csv_delimiter     = ','               if csv_delimiter      is None else csv_delimiter
#csv_quotechar     = '"'               if csv_quotechar      is None else csv_quotechar
#csv_quoting       = csv.QUOTE_MINIMAL if csv_quoting        is None else csv_quoting
csv_quoting        = csv.QUOTE_NONE    if csv_quoting        is None else csv_quoting
#csv_lineterminator= "\r\n"            if csv_lineterminator is None else csv_lineterminator

if file_input == file_output != CHAR_STD_INOUT:
    logs.error("File input '%s' can't be the same file output!" % file_input)

if args.debug >= 1:
    logs.info('run_gui            = %s' % run_gui)
    logs.info('type_input         = %s' % type_input)
    logs.info('file_input         = %s' % file_input)
    logs.info('file_output        = %s' % file_output)
    logs.info('type_output        = %s' % type_output)
    logs.info('csv_delimiter      = %s' % csv_delimiter)
    logs.info('csv_quotechar      = %s' % csv_quotechar)
    logs.info('csv_lineterminator = %s' % csv_lineterminator)

root = Tk()
feet = StringVar()
meters = StringVar()

###############################################################################
def calculate():
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
        print(feet.get()+' feet is equivalent to '+meters.get()+' meters')
    except ValueError:
        pass
###############################################################################
def main_gui():
    #root = Tk()
    root.title("Feet to Meters")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    #feet = StringVar()
    #meters = StringVar()

    feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
    feet_entry.grid(column=2, row=1, sticky=(W, E))

    ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
    ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

    ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
    ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
    ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    feet_entry.focus()
    root.bind('<Return>', calculate)

    root.mainloop()

###############################################################################
def main():
    if run_gui:
        main_gui()
        sys.exit(0)

    txt_lines = read_filein()

    dat_lines = None
    if type_input ==  TYPE_IN_av8p:
        dat_lines = manipulate_av8p(txt_lines)
    else:
        logs.error("Type input '%s' can't be configurate!" % type_input)

    write_fileout(dat_lines)

    sys.exit(0)

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

    fld_first  = 45;
    fld_code   = 10;
    fld_name   = fld_first - fld_code;
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
            print("|"+txt_line)
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
                print("#1#" + row_body_2)
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
            print("#2#" + txt_line)
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
    r = csv_delimiter;
    f = fld_first;
    l = length;
    s = step;
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
    txt_filename = file_input

    filein = None
    std_in = False
    if txt_filename == CHAR_STD_INOUT:
        filein = sys.stdin
        std_in = True
        logs.info('Read txt rows on STDIN:')
    else:
        if not _fileExist(txt_filename):
            logs.error("Can't read file '%s', exist?" % txt_filename)
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
    txt_filename = file_input
    out_filename = file_output

    fileout = None
    std_out = False
    typeout = type_output
    if out_filename == CHAR_STD_INOUT:
        fileout = sys.stdout
        typeout = TYPE_OUT_csv
        std_out = True
        logs.info('Write csv rows on STDOUT:')
    else:
        try:
            fileout = open(out_filename, 'w')
            logs.info('Write to file out: %s' % out_filename)
        except:
            fileout = sys.stdout
            std_out = True
            logs.info('File out not set, write on STDOUT:')

    name_ws = 'Report'
    if txt_filename != CHAR_STD_INOUT:
        name_ws = name_output

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
    out_filename = file_output

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