#!/usr/bin/env python
import getopt
import sys
import argparse
import time
import md5

parser = argparse.ArgumentParser(description="Find the secret code based on system time")
currentTime = "2015 01 01 00 01 30"
parser.add_argument("-c", default=currentTime, help = "Current system time. Specify only when debugging.")
args = parser.parse_args()
currentTime = args.c

DEBUG = False #If true, use a specific time (for debugging from PDF). Otherwise use -actual- system time
#Use True for labs and Cyberstorm

epochTime = raw_input()

epochTimeComponent = epochTime.split(" ")

epochTimeStruct = time.localtime(time.mktime(time.strptime(epochTime ,"%Y %m %d %H %M %S")))


#epochTimeStruct = time.gmtime(time.mktime(time.strptime(epochTime ,"%Y %m %d %H %M %S")))

epochTimeSecs = time.mktime(epochTimeStruct)

if (epochTimeStruct.tm_isdst == 1):
	pass


currentTimeStruct = time.localtime(time.time())



if (DEBUG):
	print("debug mode")
	currentTimeStruct = time.localtime(time.mktime(time.strptime(currentTime, "%Y %m %d %H %M %S")))

currentTimeSecs = time.mktime(currentTimeStruct)

if (currentTimeStruct.tm_isdst == 1):
	pass
	#currentTimeSecs += 3600


deltaTime = int(currentTimeSecs - epochTimeSecs)

deltaTime = deltaTime - (deltaTime % 60)

hash1 = md5.new()
hash1.update(str(deltaTime))

hash2 = md5.new()
hash2.update(hash1.hexdigest())

hashString = hash2.hexdigest()	

print(hashString)

code = ""

for i in hashString:
	if i.isalpha():
		code += i
	if len(code) == 2:
		break
		
for i in reversed(hashString):
	if not i.isalpha():
		code += i
	if len(code) == 4:
		break
		
print(code)
