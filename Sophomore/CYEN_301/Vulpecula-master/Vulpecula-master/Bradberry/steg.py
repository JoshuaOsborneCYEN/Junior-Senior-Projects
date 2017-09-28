#!/usr/bin/env python

import sys
import argparse

parser = argparse.ArgumentParser(description='Hide file inside wrapper file', conflict_handler='resolve')

BbGroup = parser.add_mutually_exclusive_group(required=True)
BbGroup.add_argument('-b', action='store_true', default=False, help='Store/Retrieve information using LSB')
BbGroup.add_argument('-B', action='store_true', default=False, help='Store/Retrieve information using byte')

RwGroup = parser.add_mutually_exclusive_group(required=True)
RwGroup.add_argument('-s', action='store_true', default=False, help='Store hidden file in wrapper file')
RwGroup.add_argument('-r', action='store_true', default=False, help='Extract hidden file from wrapper file')

parser.add_argument('-o', action='store', dest='offset', required=True, type=int, help='Set offset to OFFSET')
parser.add_argument('-i', action='store', dest='interval', type=int, default=1, help='Set interval to INTERVAL')
parser.add_argument('-w', action='store', dest='wrapper_file', required=True, help='Path to wrapper file')
parser.add_argument('-h', action='store', dest='hidden_file', default='', help='Path to hidden file')


args = parser.parse_args()
    
lsb = args.b    
store = args.s
offset = args.offset
interval = args.interval

wrapper_file = open(args.wrapper_file, 'r')
try:
    wrapper = bytearray(wrapper_file.read())
except:
    pass
wrapper_file.close()

if args.hidden_file != '':
    hidden_file = open(args.hidden_file, 'r')
    try:
        hidden = bytearray(hidden_file.read())
    except:
        pass
    hidden_file.close()

# 6 byte EOF string
sentinel = "\x00\xff\x00\x00\xff\x00"

if store:
    if lsb:
        # Check to make sure the hidden file will fit
        required_size = offset + 8 * interval * len(hidden) + len(sentinel)
        if len(wrapper) < required_size:
            print("Insufficient wrapper size. For hidden file of size {}, interval of {}, and offset of {},"
                   " wrapper file of size {} is required.".format(len(hidden), interval, offset, required_size))
            quit()

        # Do Least Significant Bit steg
        hidden += sentinel
        
        # For each byte of hidden...
        for i in range(len(hidden)):
            # And each bit of that byte...
            for j in range(8):
                # Set LSB of location(beginning at offset) to next bit of hidden
                wrapper[offset] &= 0xFE 
                wrapper[offset] |= (hidden[i] & 0x80) >> 7

                # Prepare next bit of hidden
                hidden[i] = (hidden[i] & 0x7F) << 1

                # Set next location
                offset += interval
        print(str(wrapper))

    else:
        # Check to make sure the hidden file will fit
        required_size = offset + interval * len(hidden) + len(sentinel)
        if len(wrapper) < required_size:
            print("Insufficient wrapper size. For hidden file of size {}, interval of {}, and offset of {},"
                  " wrapper file of size {} is required.".format(len(hidden), interval, offset, required_size))
            quit()

        # Do Bytewise steg
        hidden += sentinel
        
        #For each byte in hidden...
        for B in hidden:
            # Set byte at location(beginning at offset) to hidden byte
            wrapper[offset] = B

            # Set next location
            offset += interval

        print(str(wrapper))
else:
    if lsb:
        decoded = ""

        # Until sentinel bytes are reached, read into decoded
        while decoded[-len(sentinel):] != sentinel:
            nextb = 0
            for i in range(8):
                # Left-shift the next byte
                nextb <<=1

                # Add LSB of byte at location(beginning at offset) to next byte
                nextb += wrapper[offset] & 0x01

                # Set next
                offset += interval

            decoded += chr(nextb)

        # Print decoded file to stdout without the sentinal bytes
        print(decoded[:-len(sentinel)])
    else:
        decoded = ""

        # Until sentinel bytes are reached, read into decoded
        while decoded[-len(sentinel):] != sentinel:
            # Add byte at location(beginning at offset) into decoded
            decoded += chr(wrapper[offset])

            # Set next location
            offset += interval

        # Print decoded file to stdout without the sentinel bytes
        print(decoded[:-len(sentinel)])

