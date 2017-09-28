#!/usr/bin/env python
import ftplib
import getopt
import sys
import argparse

#Initialize argument parser
parser = argparse.ArgumentParser(description="Read FTP storage covert channel.")
#Change the default here if you want to hardcode the FTP server IP
parser.add_argument("-s", default="jeangourd.com",  help = "FTP server to get listing from (IP address or website name)")
#Argument to change FTP directory on server
parser.add_argument("-d", default="", help = "FTP directory to get listing from, default is root")
args = parser.parse_args()

#Place IP of target FTP server here
ftp = ftplib.FTP(args.s)
ftp.login("anonymous", "")

data = []

#Change directory on server
if(args.d != ""):
	ftp.cwd(args.d)
#Places list contents of FTP server in data list
ftp.dir(data.append)

#Close connection
ftp.quit()

#We only want the first 10 characters of each line
for i in range(len(data)):
	data[i] = data[i][0:10]

#7 bit binary
ASCIIType = 7

#Converts a list of file permissions into binary, then to plaintext
#Hyphens are zeroes, everything else is a one
def binaryDecode(fileList, ASCIIType):
	#Define variables
	binary = ""
	plaintext = ""
	#go over each listing (should look like drw-r--r-- e.g.)
	for item in fileList:
		#convert to binary: hyphen is 0, anything else is 1
		for char in item:
			if char == "-":
				binary += "0"
			else:
				binary += "1"
	#split into lists of size ASCIIType
	binaryList = [binary[i:i + ASCIIType] for i in range(0, len(binary), ASCIIType)]
	
	if (binaryList == []):	
		return plaintext

	#each element in this list should be 1 ASCII character
	#but first we may need to pad the last element with zeroes
	while (len(binaryList[-1:][0]) != ASCIIType):
		paddedBin = binaryList[-1:][0] + "0"
		binaryList[-1] = paddedBin
	#convert each element to binary
	for i in binaryList:
		plaintext += chr(int(i, 2))
	return plaintext



def sevenPermDecode(flist):
	newList = []
	ASCIIType = 7
	#Create a new list, each entry is a 2-item list: 
	#[first 3 characters, last 7 chars]
	for d in flist:
		n = [d[:3],d[3:]] 
		newList.append(n)
	#Remove noise (entries containing letters in first 3 chars)
	fixedList = []
	for i in range(len(newList)):
		if newList[i][0] == ( "---" ):
			fixedList.append(newList[i][1])
	#Now decode message: assume hyphens are 0, anything else is 1
	plaintext = binaryDecode(fixedList, ASCIIType)

	return plaintext

def tenPermDecode(flist):
	#Define variables
	ASCIIType = 7
	#Decode
	plaintext = binaryDecode(flist, ASCIIType)

	return plaintext 

#Here you can choose to decode the last 7 permissions or use all ten.
print sevenPermDecode(data)
print tenPermDecode(data)
