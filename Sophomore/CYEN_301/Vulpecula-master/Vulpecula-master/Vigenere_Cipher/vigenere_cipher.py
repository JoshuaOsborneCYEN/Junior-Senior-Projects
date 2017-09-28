#!/usr/bin/env python

# George Cazenavette
# 3/38/17
# python 2.7



import sys


def encode(plain, key):	# encoding function
		cipher = ""
		upperKey = key.upper()	# created an all upper case version of the key
		upperPlain = plain.upper()	# creates an all upper case version of the plain text
		j = 0
		for i in range (len(plain)):	# iterates through every character of the plain text
				if ((ord(upperPlain[i]) - 65) >= 0 and (ord(upperPlain[i]) - 65) <= 25):	# If the character is in the range A-Z
						nextChar = chr(((ord(upperPlain[i]) - 65) + (ord(upperKey[j % len(key)]) - 65)) % 26 + 65)	# Calculate the cipher chatacter based on the key
						if (plain[i].isupper()):	# If the original character is upper case...
								cipher += nextChar	# add the calculated upper case character
						else:
								cipher += nextChar.lower()	# if not, convert it to lower case
				
				else:	# if the character is not in the range A-Z
						j -= 1	# do not increment the key
						cipher += upperPlain[i]	# just print the original character
				j += 1	# increment the key index
		print(cipher)	# print the cipher text


def decode(cipher, key):	# decoding function
		plain = ""
		upperKey = key.upper()	# creates an all upper case version of the key
		upperCipher = cipher.upper()	# creates an all upper case version of the ciher text
		j = 0
		for i in range(len(cipher)):	# itterates through every character in the cipher text
				if ((ord(upperCipher[i]) - 65) >= 0 and (ord(upperCipher[i]) - 65) <= 25):	# If the character is in the range A-Z
						nextChar = chr(((ord(upperCipher[i]) - 65) - (ord(upperKey[j % len(key)]) - 65) + 26) % 26 + 65)	# calculate the plain text character based on the key
						if (cipher[i].isupper()):	# if the original character is upper case..
								plain += nextChar	# add the calculated upper case character
						else:
								plain += nextChar.lower()	# if not, convert it to lower case
				
				else:	# if the character is not in the range A-Z
						j -= 1	# do not increment the key
						plain += upperCipher[i]	# just print the original character
				j += 1	# increment the key index
		print(plain)	# print the plain text





if (len(sys.argv) != 3 or not(sys.argv[1] == "-e" or sys.argv[1] == "-d")):	# checks to see if the arguments are valid
		print("Invalid Parameters")
		sys.exit()

mode = sys.argv[1]	
key = sys.argv[2]
key = key.replace(" ","")
key = key.replace("\t","")



while (True):
		try:	
				inputString = raw_input()	# takes unput from stdin
		except EOFError:	# exits program if ^D is pressed or EOF is reached
				sys.exit()

		if (mode == "-e"):
				encode(inputString, key) 	# encoding
		else:
				decode(inputString, key)	# decoding

