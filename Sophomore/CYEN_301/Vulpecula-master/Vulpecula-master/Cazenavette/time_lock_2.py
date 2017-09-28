#!/usr/bin/env python

DEBUG = False
currentTime = "2017 04 26 15 14 30"

import time
import md5
import sys
import datetime



epochTime = raw_input()

epochTimeComponent = epochTime.split(" ")


epochTimeStruct = datetime.datetime.strptime(epochTime + " " + time.tzname[1],"%Y %m %d %H %M %S %Z")



print(epochTimeStruct)



currentTimeStruct = datetime.datetime.today()




deltaTime = (currentTimeStruct - epochTimeStruct).total_seconds()


if (DEBUG):
	print("debug mode")
	currentTimeStruct = datetime.datetime.strptime(currentTime, "%Y %m %d %H %M %S")
	

	
print(currentTimeStruct)
	
deltaTime = (currentTimeStruct - epochTimeStruct).total_seconds()





deltaTime = int(deltaTime - (deltaTime % 60))

print(deltaTime)

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
