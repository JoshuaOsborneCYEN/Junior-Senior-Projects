import base64
import binascii
import hashlib

class DocInfo:

    def __init__(self):
        this.carvedFile = open("carvedFILE.extunknown", "wb")

    def __init__(self, header, footer, type):
        this.header = header
        this.footer = footer
        this.type = type
        this.carvedFile = open("carved" + type.upper() + "." + type.lower(), "wb")


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
#DOCF = "07000000ffff0300"
DOCF = "4707863767662212132402324257e5e21"

hashList = ["c3a04e65e43b4a862b010927fae9aab1",
    "3b2f3b12ee4b04d4d0384adeee21e4d4",
    "06d08f17d7b2efbc0dc0d303398196d0",
    "aec49002f8b02c2099152df1ec18b6c1"]


def checkHash( fileString, name = "FILE"):
    m = hashlib.md5()
    m.update(fileString)
    hashString = m.hexdigest()
    print hashString
    if hashString in hashList:
        print ("File hash for " + name + " checks out.")
    else:
        print (name + " not in hash list.")



#first decode the file from base64 into ASCII
corrupted_file = open("corrupted.docx", "rb")
corrupted_read = corrupted_file.read()
corrupted_ascii = base64.decodestring(corrupted_read)
#corrupted = corrupted_ascii.read()
#print corrupted_ascii
corrupted = corrupted_ascii.encode("hex")
#corrupted = "test".encode("hex")
corrupted_result = open("corrupted_hex.txt", "wb")
corrupted_result.write(corrupted)
#print corrupted

carvedPDF = open("carvedPDF.pdf", "wb")
carvedGIF = open("carvedGIF.gif", "wb")
carvedJPG = open("carvedJPG.jpg", "wb")
carvedPNG = open("carvedPNG.png", "wb")
carvedDOC = open("carvedDOC.doc", "wb")

def carve(header, footer, writeFile, name = "FILE"):
    fileStart = corrupted.find(header)
    if (type(footer) is int):
        fileEnd = footer
    else:
        fileEnd = fileStart + corrupted[fileStart:].find(footer)
    if (fileStart != -1 and fileEnd != -1):
        if (type(footer) is int):
            fileHex = corrupted[fileStart:fileEnd]
        else:
            fileHex = corrupted[fileStart:fileEnd + len(footer)]
        fileText = fileHex.decode("hex")
        writeFile.write(fileText)
        checkHash(fileText, name)
    else:
        print (name + " not found!")

carve(PDFH, PDFF, carvedPDF, "PDF")
carve(PNGH, PNGF, carvedPNG, "PNG")
carve(GIFH, GIFF, carvedGIF, "GIF")
carve(JPGH, JPGF, carvedJPG, "JPG")
carve(DOCH, DOCF, carvedDOC, "DOC")

"""
pngStart = corrupted.find(PNGH)
pngEnd = corrupted.find(PNGF)
if (pngStart != -1 and pngEnd != -1):
    pngHex = corrupted[pngStart:pngEnd + len(PNGF)]
    pngText = pngHex.decode("hex")
"""
