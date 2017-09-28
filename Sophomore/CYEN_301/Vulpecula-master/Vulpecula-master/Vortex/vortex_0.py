#!/usr/bin/env python

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# sets up a socket with specific parameters
s.connect(('vortex.labs.overthewire.org',5842))			# creates a socket connection to the port
total = 0
for i in range(4):		# 4 integers
		for j in range(4):	# 4 bytes per integer
				byte = s.recv(1)	# recieve one byte at a time
				total += ((ord(byte) << (8 * j)))	# shift it by the appropriate number of bits and add to total

returnString = ""	# prepares the return message

for i in range(4):	# 4 bytes in sum integer
		returnString += chr((total >> 8 * i)  & 0xFF)	# shift bytes and convert to character then append to string
s.send(returnString)	# send the return string

print(s.recv(1024))	# recieve the response and print it
