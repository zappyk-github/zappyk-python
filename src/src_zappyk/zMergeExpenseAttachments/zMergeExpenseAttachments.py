
# Importing modules:
import os
import sys
import pathlib
import shutil
from zipfile import ZipFile
from xml.dom import minidom
from PIL import Image
from pypdf import PdfMerger

_devel = True
_debug = 2

fileZipName = None
pathZipBase = None
pathZipWork = None

"""
defined function main
"""
def main():
    global fileZipName, pathZipBase, pathZipWork
    
    thisFile = 'Note spese . expertise da 34 a 39.zip'
    thisPath = pathlib.Path(__file__).parent.resolve()
    tempPath = 'tmp'
    
    print("Init:")
    
    try:
        fileZipName = sys.argv[1]
    except:
        if not(_devel):
            print("Specifica un file ZIP")
            exit(1)
        else:
            fileZipName = os.path.join(thisPath, thisFile)
        
    try:
        pathZipWork = sys.argv[2]
    except:
        pathZipBase = os.path.join(pathlib.Path.home().drive, os.sep, tempPath, os.path.basename(os.path.splitext(pathlib.Path(__file__))[0]))
        pathZipWork = os.path.join(pathZipBase, os.path.basename(os.path.splitext(fileZipName)[0]))

    if _debug >= 1:
        print("· this direc.: %s" % str(thisPath))
        print("· fileZipName: %s" % fileZipName)
        print("· pathZipBase: %s" % pathZipBase)
        print("· pathZipWork: %s" % pathZipWork)
    #exit(0)
    
    print("Process...")
    extractZip()
    readFileXml()

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
                
            # Create name for file attachements
            keysNameAttached = '_'.join([_ANNONS+_MESE.rjust(2, '0'), _IDCOMPANY, _IDEMPLOY, _CFISC, _NRNOTASPESE, _NOMINATIVO])
            keysFileAttached = os.path.join(pathZipWork, keysNameAttached) + '.pdf'
            baseNameAttached = '_'.join([_BaseName, keysNameAttached])
            baseFileAttached = os.path.join(pathZipWork, baseNameAttached) + '.pdf'
            print(" · base %s" % baseFileAttached)
            print(" · keys %s" % keysFileAttached)
            
            convertImage2PDF2Merge(fileNameLnk, baseFileAttached, keysFileAttached)

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
        print("Open file image: %s" % fileImage)
        fileImage = Image.open(fileImage)
        
        # Write file PDF
        print("Write file PDF: %s" % filePDF)
        image = fileImage.convert('RGB')
        image.save(filePDF)

    if os.path.isfile(mergePDF):
        print("Merge file PDF...")
        pdfFiles = [mergePDF, filePDF]
        pdfMerger = PdfMerger()
        for pdf in pdfFiles:
            pdfMerger.append(pdf)
        pdfMerger.write(mergePDF)
        pdfMerger.close()
    else:
        print("Merge file PDF (first)")
        shutil.copy(filePDF, mergePDF)

# Entry point
if __name__ == '__main__':
    main()
    
exit(0)