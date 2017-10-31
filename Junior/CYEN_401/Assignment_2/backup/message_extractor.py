#!/usr/bin/env python

"""
This program should write 6 files to the current directory.

Given the names of each file to be scanned via LSB decryption in the imageList
list, this program scans through the LSB of each color of each pixel, one color
at a time. For each color scanned, it will write the results of the decoded
file to the current directory. Thus there will be 3 output files per input
file representing each of the RGB colors. They will share the same name
as the input picture, except the extension will be replaced with 'Decode' and
the number representing the color decoded: 0 for red, 1 for green, and 2 for
blue.
"""


from PIL import Image
from PIL import ImageFilter
import binascii

imageList = ["mountain (copy).png", "DCIM_2837.png"]

#scan each image
for image in imageList:
    im = Image.open(image)
    #get pixel color values in the form of a list of lists
    rgbList = list(im.getdata())
    #red is 0, green is 1, blue is 2
    for color in range(0,3):
        #string of zeroes and ones, refreshed for each color
        bitString = ""
        #iterate over every pixel
        for pixel in rgbList:
            if pixel[color] % 2 == 0: #val is even, LSB is 0
                bitString += "0"
            else: #val is odd, LSB is 1
                bitString += "1"
        #convert binary to hex then to ascii
        text = binascii.unhexlify('%x' % int(bitString, 2))
        #name decoded file after the original image and color decoded
        output_file = open(image[:-4] + "Decode" + str(color), "w")
        output_file.write(text)
        output_file.close()
