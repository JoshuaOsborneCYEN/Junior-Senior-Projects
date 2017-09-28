#!/usr/bin/python

import getopt
import sys
import argparse

#Initialize argument parser
parser = argparse.ArgumentParser(description="Encode or decode a message")
parser.add_argument("-e", default="",  help = "Encode message using specified key")
parser.add_argument("-d", default="", help = "Decode message using specified key")

def encode(message):
	"""Encode vigenere message: accept user input, encode with key,
	print encoded message"""
	key = args.e #Sets key as given after -e arg
	key = key.replace(" ", "") #Remove whitespace
	ciphertext = "" #Initialize
	k = 0 #Key iterator
	for m in message:
		if (not m.isalpha()): #not a letter
			ciphertext += m #move on to next message letter
		else:
			if m.isupper(): #Upper case character
				#Takes ASCII numeric value of key, adds the Vig. cipher key,
				#then subtracts the offset from 0 in order to mod 26, finally
				#adding the offset back and finding the character.
				ciphertext += chr( ( (ord(m) + ord(key[k].upper()) ) - 65 * 2 ) %  26 + 65 )
			else: #Lower case character
				ciphertext += chr( ( (ord(m) + ord(key[k].upper()) ) - 97 - 65 ) %  26 + 97 )

			k = (k + 1) % len(key) #Go to next letter in key
	return ciphertext

def decode(message):
	"""Decode vigenere message: accept user input, decode with key,
	print decoded message"""
	key = args.d #key given after -d
	key = key.replace(" ", "") #remove whitespace
	plaintext = ""
	k = 0 #Key iterator
	for m in message:
		if (not m.isalpha()): #message character is not a letter
			plaintext += m #move to next char in message
		else:
			if m.isupper(): #Upper case character
				#Takes ASCII numeric value of key, subtracts the Vig. cipher key,
				#then subtracts the offset from 0 in order to mod 26, finally
				#adding the offset back and finding the character.
				plaintext += chr( ( (ord(m) - ord(key[k].upper()) ) - 65 * 2 + 26 ) %  26 + 65 )
			else: #Lower case character
				plaintext += chr( ( (ord(m) - ord(key[k].upper()) ) - 97 - 65 + 26 ) %  26 + 97 )

			k = (k + 1) % len(key) #Go to next letter in key
	return plaintext 


args = parser.parse_args()
#args stored in args.e and args.d
#-e used: encode
if (args.e != "" and args.d == ""):
	while(1):
		try:
			#capable of encoding line after line
			ciphertext = encode(raw_input())
			print ciphertext
		except EOFError as e:
			sys.exit()
#-d used: decode
if (args.e == "" and args.d != ""):
	while(1):
		try:
			#capable of decoding line after line
			ciphertext = decode(raw_input())
			print ciphertext
		except EOFError as e:
			sys.exit()
