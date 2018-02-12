#!/usr/bin/env python
#word is 2 bytes
#double word is 4 bytes
IMAGE = "Image.img"
#question 2-7
LOOKUP_VALS = [
("2. Bytes per sector: " , "0B", 2),
("3. Sectors per cluster: " , "0D", 1),
("4. Reserved sector count: " , "0E", 2),
("5. Number of FATs: " , "10", 1),
("6. Maximum Root Directory Entries: " , "11", 2),
("7. Sectors per FAT: " , "16", 2)
]

image = open(IMAGE, "rb")
image_hex = image.read().encode("hex")
def dehex(inputString):
    return int(inputString)

def decodeFromOffset(offset, length):
    offsetIndex = int(offset, 16) * 2
    big_endian = image_hex[offsetIndex:offsetIndex + length * 2]
    little_endian = ""
    for i in range(0, len(big_endian), 2):
        little_endian = (big_endian[i: i+2]) + little_endian
    return str(int(little_endian, 16))



resultDict = {}
for item in LOOKUP_VALS:
    data = (decodeFromOffset(item[1], item[2]) )
    #updates result dict with number of question and the solution
    resultDict[ int( item[0][0: item[0].find(".") ] ) ] = data

BOOT_SECTOR_SIZE = str(int(resultDict[2]))

#solving questions
print ("1. Boot block (Master Boot Record) occupies " + BOOT_SECTOR_SIZE + " bytes")
    #index 0 is bytes per sector, 1 is
for item in LOOKUP_VALS:
    data = (decodeFromOffset(item[1], item[2]))
    print (item[0] + data)
#first fat comes right after the boot sector
print ("8. Byte offset of first FAT: " + BOOT_SECTOR_SIZE)
#second fat comes after first
secondFatOffset = int(BOOT_SECTOR_SIZE) + int(resultDict[2]) * int(resultDict[7])
print ("9. Byte offset of second FAT: " + str(secondFatOffset) )
#root offset = bytes/sector * sectors/fat * # fats + first offset
rootDirectoryOffset = int(resultDict[2]) * int(resultDict[5]) * int(resultDict[7]) + int(BOOT_SECTOR_SIZE)
print ("10. Byte offset of root directory: " + str(rootDirectoryOffset))
#data block offset = root directory offset + (32 bytes * number of root entries)
dataBlockOffset = rootDirectoryOffset + 32 * int(resultDict[6])
print ("11. First data block offset: " + str(dataBlockOffset))
print ("12. Total data region size: " + str( len(image_hex)/2 - dataBlockOffset))


#find start using header (magic number)
fileStart = image_hex.find("ffd8")
#find end of file, sometimes footer is hardcoded if it is not standardized
fileEnd = fileStart + image_hex[fileStart:].find("ffd9")

if (fileStart != -1 and fileEnd != -1):
    #first make sure those numbers were found
    #extract hex
    fileHex = image_hex[fileStart:fileEnd + len("ffd9")]
    #decode hex
    fileText = fileHex.decode("hex")
    #write to file
    output = open("output.jpg", "w")
    output.write(fileText)
else:
    #error has occurred; magic numbers not in list
    print ("JPEG not found!")

#find start using header (magic number)
fileStart_2 = fileEnd + image_hex[fileEnd:].find("ffd8")
#find end of file, sometimes footer is hardcoded if it is not standardized
fileEnd_2 = fileStart_2  + image_hex[fileStart_2:].find("a6cfffd9")

if (fileStart != -1 and fileEnd != -1):
    #first make sure those numbers were found
    #extract hex
    fileHex = image_hex[fileStart_2:fileEnd_2 + len("a6cfffd9")]
    #decode hex
    fileText = fileHex.decode("hex")
    #write to file
    output = open("output-2.jpg", "w")
    output.write(fileText)
else:
    #error has occurred; magic numbers not in list
    print ("JPEG not found!")
