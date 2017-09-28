#!/usr/bin/env python


DEFAULT_DOMAIN = "localhost"
DEFAULT_PORT = 1337
BIT_SIZE = 8
LONG = "0"
SHORT = "1"


import socket
import sys
import time


def variance(varList):
		#print(len(varList))
		if (len(varList) == 0 or len(varList) == 1):
				return 0.0
		#print(varList[:][1])
		average = sum(map(lambda x: x[1], varList)) / float(len(varList))
		varSum = 0
		for i in range(len(varList)):
				varSum += (varList[i][1] - average) ** 2
		var = varSum / (float(len(varList)) - 1.0)
		return var



if (len(sys.argv) != 3):
		print("using default parameters")
		DOMAIN = DEFAULT_DOMAIN
		PORT = DEFAULT_PORT
else:
		DOMAIN = sys.argv[1]
		PORT = int(sys.argv[2])




try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((DOMAIN, PORT))
except Exception:
		print("not able to establish connection on specified domain and port")
		print("1st parameter should be domain")
		print("2nd parameter should be port")
		sys.exit(0)

covert_bin = ""
timeList = []
timeIndex = 0



data = s.recv(4096)


while (data.rstrip() != "EOF"):
		sys.stdout.write(data)
		sys.stdout.flush()
		t0 = time.time()
		data = s.recv(4096)
		t1 = time.time()
		timeList.append([timeIndex, t1-t0, ""])
		timeIndex += 1
s.close()

lowerList = timeList[:]
upperList = []

lowerList.sort(key = lambda x: float(x[1]))

minVar = variance(lowerList) + variance(upperList)
bestLower = lowerList
bestUpper = upperList

for i in range(len(timeList)):
		
		upperList.insert(0, lowerList.pop())
		
		if (variance(lowerList) + variance(upperList) < minVar):
				
				
				minVar = variance(lowerList) + variance(upperList)
				bestLower = lowerList[:]
				bestUpper = upperList[:]

for element in bestUpper:
		element[2] = LONG

for element in bestLower:
		element[2] = SHORT


grandList = lowerList + upperList
grandList.sort(key = lambda x: int(x[0]))

covert_bin = ""

for element in grandList:
		covert_bin += element[2]

covert_msg = ""



i = 0
while (i + BIT_SIZE  <= len(covert_bin)):
		covert_msg += chr(int(covert_bin[i : i + BIT_SIZE], 2))
		if (covert_msg.find("EOF") != -1):
				break
		i += BIT_SIZE

covert_msg = covert_msg.rstrip("EOF")

print("\nCovert message: " + covert_msg)
