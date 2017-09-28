"""Resources used:      https://www.tutorialspoint.com/python/python_networking.htm
                        https://docs.python.org/3.0/library/socket.html
                        https://docs.python.org/3/library/struct.html """
import socket
import struct

#Get a socket to communicate with
s = socket.socket()

#Connect to the required server at the specified port (function takes a tuple, not two distinct values)
s.connect(("vortex.labs.overthewire.org", 5842))

#Add up the 4 integers that are received and unpacked as unsigned ints in little endian (The "<I" part)
total = sum(struct.unpack("<I", s.recv(4))[0] for _ in range(4))

#Send back the total, packed as an unisgned int and forced to be 4 bytes long (bitwise & 0xFFFFFFFF)
s.send(struct.pack("<I", total & 0xFFFFFFFF));

#Receive reply and print
print(s.recv(1024))

#Clean up
s.close()
