#!/usr/bin/python
"""Your goal is to connect to port 5842 on vortex.labs.overthewire.org 
and read in 4 unsigned integers in host byte order. 
Add these integers together and send back the results 
to get a username and password for vortex1.
This information can be used to log in using SSH.

Note: vortex is on an 32bit x86 machine 
(meaning, a little endian architecture)"""
import socket
import struct

#Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connect to the required server @ port
s.connect(("vortex.labs.overthewire.org", 5842))

intList = []

for i in range(4):
	byte0 = s.recv(1)
	byte1 = s.recv(1)
	byte2 = s.recv(1)
	byte3 = s.recv(1)

	#byteValues = [byte3, byte2, byte1, byte0]
	byteValues = [byte0, byte1, byte2, byte3]
	newInt = struct.unpack("I", bytearray(byteValues))[0]
	intList.append(newInt)

total = 0
for i in intList:
	total += i

s.send(struct.pack("I", (total & 0xFFFFFFFF)))
print s.recv(1024)
#print intList
#s.shutdown()
s.close()

