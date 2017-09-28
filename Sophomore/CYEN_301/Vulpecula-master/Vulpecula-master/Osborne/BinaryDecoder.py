#!/usr/bin/python

import sys

binary = sys.stdin.read()
#To rid the newline at end of input from the count
length = len(binary) - 1

divByBoth = 0

def findASCIIType(inputLength):
	"""This function tries to find whether the input is 7 bit or 8 bit ASCII""" 
	if (inputLength % 8 == 0) and (length % 7 == 0):
		#Divisible by 8 AND 7
		#Assume it's 8 first, then check in the convert function later
		#Assumption will be changed if any value is unreadable
		#That is, if int(<8 bits>) > 127
		divByBoth = 1
		return 8
	elif (inputLength % 8 == 0):
		return 8
	elif (inputLength % 7 == 0):
		return 7
	else:
		print "Invalid number of binary characters"
		return -1

def convert(charList):
	"""This function converts the divided list of binary numbers into a string of readable characters"""
	output = ""
	if len(charList[0]) == 7:
		for char in charList:
			output += chr(int(char, 2))

	elif len(charList[0]) == 8:
		for char in charList: 
			output += chr(int(char, 2))
	
	elif (len(charList[0]) == 8 and divByBoth == 1):
		for char in charList: 
			if (int(char, 2) > 127):
				return ""
			output += chr(int(char, 2))
		divByBoth == 0 #signals later that we do not need to try again and interpret with 7 bits
	return output

#Determines whether ASCII is 8 bit or 7 bit type
ASCIIType = findASCIIType(length)

#Initialize ASCII character list
characterList = []

output = ""

#ensure there's not an error
if ASCIIType != -1:
	#splits the list into sections of 7 or 8. 
	#syntax: for loop that adds i to i+ASCIIType (8 or 7) each iteration.
	characterList = [binary[i:i + ASCIIType] for i in range(0, len(binary), ASCIIType)]
	if (divByBoth == 1):
		#failed to make readable text assuming 8 bit ASCII; try 7 bit
		characterList = [binary[i:i + 7] for i in range(0, len(binary), 7)]
	characterList.remove("\n")
	output = convert(characterList)
else:
	print "The binary could not be read (# binary characters is not divisible by 8 or 7)"
print output
