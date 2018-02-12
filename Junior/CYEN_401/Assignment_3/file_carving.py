#!/usr/bin/env python
import base64
import binascii
import hashlib

#name of corrupted file in current directory
CORRUPTED_NAME = "corrupted.docx"

#define magic numbers in hex
PDFH = "25504446"
PDFF = "2525454f460a"
GIFH = "47494638"
GIFF = "5a00003b"
JPGH = "ffd8ffe0"
JPGF = "ffd9"
PNGH = "89504e47"
PNGF = "4e44ae426082"
DOCH = "504b0304"
DOCF = "4707863767662212132402324257e5e21"

#we check our files to make sure they are correct against this list
hashList = ["c3a04e65e43b4a862b010927fae9aab1",
    "3b2f3b12ee4b04d4d0384adeee21e4d4",
    "06d08f17d7b2efbc0dc0d303398196d0",
    "aec49002f8b02c2099152df1ec18b6c1"]

#holder class for document info
#makes it easier to contain data on files we are looking to extract
class DocInfo:
    #do not use default
    def __init__(self):
        self.carvedFile = open("carvedFILE.extunknown", "wb")

    #initialize DocInfo with header, footer, and type (which determines file name)
    def __init__(self, header, footer, type):
        self.header = header
        self.footer = footer
        self.type = type
        #create file to write carved ASCII to
        self.carvedFile = open("carved" + type.upper() + "." + type.lower(), "wb")

    #creates a list to better communicate with Carve function
    #deprecated
    def listAttributes(self):
        return [self.header, self.footer, self.carvedFile, self.type]

    #carve function finds file using header and footer and extracts it
    def carve(self, hexBlock):
        #find start using header (magic number)
        fileStart = hexBlock.find(self.header)
        #find end of file, sometimes footer is hardcoded if it is not standardized
        fileEnd = fileStart + hexBlock[fileStart:].find(self.footer)

        if (fileStart != -1 and fileEnd != -1):
            #first make sure those numbers were found
            #extract hex
            fileHex = hexBlock[fileStart:fileEnd + len(self.footer)]
            #decode hex
            fileText = fileHex.decode("hex")
            #write to file
            self.carvedFile.write(fileText)
            checkHash(fileText, self.type)
        else:
            #error has occurred; magic numbers not in list
            print (name + " not found!")

#checks md5 hash of file string against our list
def checkHash( fileString, name = "FILE"):
    m = hashlib.md5()
    m.update(fileString)
    hashString = m.hexdigest()
    if hashString in hashList:
        print ("File hash for " + name + " checks out.")
    else:
        print (name + " not in hash list.")
    print (hashString)

#prepare list of document info
docList = []
docList.append( DocInfo(PDFH, PDFF, "PDF"))
docList.append( DocInfo(GIFH, GIFF, "GIF"))
docList.append( DocInfo(JPGH, JPGF, "JPG"))
docList.append( DocInfo(PNGH, PNGF, "PNG"))
docList.append( DocInfo(DOCH, DOCF, "DOC"))

#first decode the file from base64 into ASCII
corrupted_file = open(CORRUPTED_NAME, "rb")
corrupted_read = corrupted_file.read()
corrupted_ascii = base64.decodestring(corrupted_read)
#then encode into hex to search for magic numbers
corrupted = corrupted_ascii.encode("hex")
#write hex to file for reference
corrupted_result = open("corrupted_hex.txt", "wb")
corrupted_result.write(corrupted)

#carve each document using its info from the corrupted hex block
for item in docList:
    item.carve(corrupted)
