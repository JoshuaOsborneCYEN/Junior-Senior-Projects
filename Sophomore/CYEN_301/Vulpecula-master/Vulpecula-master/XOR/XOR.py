#!/usr/bin/env python

# Vulpecula
# XOR Encryption

import sys

key_file = open("key",'r')	# opens the key file in read mode

key = key_file.read()	# reads the text from the key file

text = sys.stdin.read()	# reads the text from the input file

output = ""	# initializes the output text

for i in range(len(text)):	# iterates through every byte pair
		output += chr(ord(key[i % len(key)]) ^ ord(text[i]))	# calculates the output through XOR each byte
																# the '%' is in case we ever encounter a key shorter than the text

print(output)	# prints the output
