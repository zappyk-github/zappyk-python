# -*- coding: utf-8 -*-
__author__ = 'pes0zap'

# Importing modules:
import os
import sys
import pathlib
import shutil
from zipfile import ZipFile
from xml.dom import minidom
from PIL     import Image
from pypdf   import PdfMerger

_debug = 0
_devel = True

fileOutRepo = "Attachments"

fileZipName = None
fileZipOutR = None
pathZipName = None
pathZipBase = None
pathZipWork = None
listFileOut = {}

"""
defined function main
"""
def main():
    global fileZipName, fileZipOutR, pathZipName, pathZipBase, pathZipWork
    
    thisFileIn  = os.path.join("Note spese . expertise da 34 a 39.zip")
    thisFileOut = os.path.join(fileOutRepo+".zip")
    thisPath    = os.path.join(pathlib.Path(__file__).parent.resolve(), "resources")
    tempPath    = "tmp"
    
    print("Init:")
    
    try:
        fileZipName = sys.argv[1]
    except:
        if not(_devel):
            print("Specifica un file ZIP in input")
            exit(1)
        else:
            fileZipName = os.path.join(thisPath, thisFileIn)
    
    try:
        fileZipOutR = sys.argv[1]
    except:
        if not(_devel):
            print("Specifica il nome ZIP in output")
            exit(1)
        else:
            fileZipOutR = os.path.join(thisPath, thisFileOut)
        
    try:
        pathZipWork = sys.argv[2]
    except:
        pathZipName = os.path.basename(os.path.splitext(fileZipName)[0])
        pathZipBase = os.path.join(pathlib.Path.home().drive, os.sep, tempPath, os.path.basename(os.path.splitext(pathlib.Path(__file__))[0]))
        pathZipWork = os.path.join(pathZipBase, os.path.basename(os.path.splitext(fileZipName)[0]))

    if _debug >= 1:
        print("· d.resources: %s" % str(thisPath))
        print("· fileZipName: %s" % fileZipName)
        print("· fileZipOutR: %s" % fileZipOutR)
        print("· pathZipName: %s" % pathZipName)
        print("· pathZipBase: %s" % pathZipBase)
        print("· pathZipWork: %s" % pathZipWork)
        
    # Check to see if the ZIP file is created
    if not(os.path.exists(pathZipBase)):
        print("ATTENZIONE: directory temporanea %s non esiste!" % pathZipBase)
        exit(1)
    #exit(0)
    
    print("Process...")
    extractZip()
    readFileXml()
    createZipOut()

    print("Done.")
    
    exit(0)

"""
defined function extract items in ZIP file
"""
def extractZip():
    try:
        # Loading ZIP file...
        print("Read file ZIP: %s" % fileZipName)
        with ZipFile(fileZipName, 'r') as fz:
        
            try:
                # ...extracting all the items into a path
                print("Extract items into: %s" % pathZipWork)
                fz.extractall(path=pathZipWork)
            except:
                print("...error extract zip!")
                exit(1)
    except:
        print("...error read zip!")
        exit(1)

"""
defined function read file extract
"""
def readFileXml():
    global listFileOut
    
    # Iterate directory
    print("Read files into: %s" % pathZipWork)
    for fileItem in os.listdir(pathZipWork):
        
        fileName = os.path.join(pathZipWork, fileItem)
        fileNameLnk = os.path.splitext(fileName)[0]
        fileNameExt = os.path.basename(os.path.splitext(fileName)[1])
        
        if fileNameExt.lower() == '.xml':
            if _debug >= 2:
                print("%s: %s" % ('Read', fileName))

            # Parse an xml file by name
            fileXml = minidom.parse(fileName)
            
            # Use getElementsByTagName() to get tag
            fileXmlTag = fileXml.getElementsByTagName('attribute')
            
            _BaseName    = os.path.basename(fileNameLnk)
                                # Example:
            _ANNONS      = None # = 2023
            _CFISC       = None # = PLLFNC67A01I936L
            _CFISSOS     = None # = 02630180103
            _CPROWNUM    = None # = 4
            _DATASPESA   = None # = 20230707
            _DSTIPOPAGA  = None # = Carta di credito personale
            _DSVOCESP    = None # = Altre spese giust. e autoriz.
            _HTRDATAAPP  = None # = #
            _HTRORAAPP   = None # = #
            _HTRUSERAPP  = None # = #
            _IDCOMPANY   = None # = 000310
            _IDEMPLOY    = None # = 0000361
            _KEYATTACH   = None # = 0003102023341202307074
            _KEYATTACH2  = None # = 000310202334
            _MESE        = None # = 7
            _NOMINATIVO  = None # = PELLICANO&apos; FRANCESCO
            _NRNOTASPESE = None # = 34
            _NRTRASFERTA = None # = 1
            _TIPODOCTR   = None # = SPESE
            _TIPOPAGA    = None # = 002
            _VOCESPESA   = None # = 0013
            
            # Read all item attributes
            if _debug >= 3:
                print('Read all attributes:')
            for tag in fileXmlTag:
                fileXmlTagName = tag.attributes['name'].value
                fileXmlTagValue = tag.attributes['value'].value
                if _debug >= 3:
                    print(" · attribute %s = %s" % (fileXmlTagName, fileXmlTagValue))
                if fileXmlTagName == "ANNONS"      : _ANNONS      = fileXmlTagValue
                if fileXmlTagName == "CFISC"       : _CFISC       = fileXmlTagValue
                if fileXmlTagName == "DATASPESA"   : _DATASPESA   = fileXmlTagValue
                if fileXmlTagName == "IDCOMPANY"   : _IDCOMPANY   = fileXmlTagValue
                if fileXmlTagName == "IDEMPLOY"    : _IDEMPLOY    = fileXmlTagValue
                if fileXmlTagName == "KEYATTACH"   : _KEYATTACH   = fileXmlTagValue
                if fileXmlTagName == "MESE"        : _MESE        = fileXmlTagValue
                if fileXmlTagName == "NOMINATIVO"  : _NOMINATIVO  = fileXmlTagValue
                if fileXmlTagName == "NRNOTASPESE" : _NRNOTASPESE = fileXmlTagValue
            if _debug >= 3:
                print()

            try:
                # Create name for file attachements
                keysNameAttached = '_'.join([fileOutRepo, _ANNONS+_MESE.rjust(2, '0'), _IDCOMPANY, _IDEMPLOY, _CFISC, _NRNOTASPESE, _NOMINATIVO])
                keysFileAttached = os.path.join(pathZipWork, keysNameAttached)+'.pdf'
                baseNameAttached = '_'.join([_BaseName, keysNameAttached])
                baseFileAttached = os.path.join(pathZipWork, baseNameAttached)+'.pdf'
                if _debug >= 4:
                    print(" · base %s" % baseFileAttached)
                    print(" · keys %s" % keysFileAttached)
                    
                try:
                    convertImage2PDF2Merge(fileNameLnk, baseFileAttached, keysFileAttached)
                    listFileOut[keysFileAttached] = 1
                except:
                    print("ATTENZIONE: non è stato possibile convertire gli allegati in file PDF!")
                    print("ATTENZIONE: l'allegato è ignortato: %s" % _BaseName)
            except:
                print("ATTENZIONE: non è stato possibile ricavare tutti i valori di raggruppamento!")
                print("ATTENZIONE: l'allegato è ignortato: %s" % _BaseName)

        else:
            if _debug >= 3:
                print("%s: %s" % ('----', fileName))

"""
defined function read file extract
"""
def convertImage2PDF2Merge(fileImage, filePDF, mergePDF):
    
    fileImageExt = os.path.splitext(fileImage)[1]
    
    if fileImageExt.lower() == '.pdf':
        # Copy file PDF
        print("Copy file PDF: %s" % filePDF)
        shutil.copy(fileImage, filePDF)
        
    else:
        # Open file image
        print("Convert attach: %s" % fileImage)
        fileImage = Image.open(fileImage)
        
        # Write file PDF
        print("Write file PDF: %s" % filePDF)
        image = fileImage.convert('RGB')
        image.save(filePDF)

    if os.path.isfile(mergePDF):
        print("Merge file PDF (+ add)")
        pdfFiles = [mergePDF, filePDF]
        pdfMerger = PdfMerger()
        for pdf in pdfFiles:
            pdfMerger.append(pdf)
        pdfMerger.write(mergePDF)
        pdfMerger.close()
    else:
        print("Merge file PDF (first)")
        shutil.copy(filePDF, mergePDF)

"""
defined function read file extract
"""
def createZipOut():
    try:
        # Create ZIP output file
        print("Create file ZIP output: %s" % fileZipOutR)
        with ZipFile(fileZipOutR, 'w') as zf:
            for file in listFileOut:
                print(" · add PDF file: %s" % file)
                zf.write(file, arcname=os.path.join(pathZipName, os.path.basename(file)))
            zf.close

        # Show content ZIP output file
        print("ZIP out file contents:")
        with ZipFile(fileZipOutR, mode="r") as zf:
            zf.printdir()
    except:
        print("ZIP out file not created!")

# Entry point
if __name__ == '__main__':
    main()
    
exit(0)