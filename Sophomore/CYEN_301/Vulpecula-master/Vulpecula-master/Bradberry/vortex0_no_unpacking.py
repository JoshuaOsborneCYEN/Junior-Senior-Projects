"""Resources used:      https://www.tutorialspoint.com/python/python_networking.htm
                        https://docs.python.org/3.0/library/socket.html """
import socket

#Get a socket to communicate with
s = socket.socket()

#Connect to the required server at the specified port (function takes a tuple, not two distinct values)
s.connect(("vortex.labs.overthewire.org", 5842))

#Add up the 4 integers that are received and unpacked as unsigned ints in little endian 
total = 0

for x in range(16):
    total += ord(s.recv(1)) * 0x100 ** (x % 4)

#Send back the total, packed as an unisgned int and forced to be 4 bytes long (bitwise & 0xFFFFFFFF)
total &= 0xFFFFFFFF

return_string = ""

for _ in range(4):
    return_string += chr(total % 0x100)
    total /= 0x100

s.send(return_string);

#Receive reply and print
print(s.recv(1024))

#Clean up
s.close()
