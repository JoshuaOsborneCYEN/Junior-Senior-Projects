#!/usr/bin/env python

import hashlib
#list of lowercase letters for convenience
from string import ascii_lowercase

#list of known password hashes
hashDict = {"9aeaed51f2b0f6680c4ed4b07fb1a83c" : "Jkirk.zip",
        "172346606e1d24062e891d537e917a90" : "Lmccoy.zip",
        "fa5caf54a500bad246188a8769cb9947" : "Cchapel.zip"}

solutionFile = open("passwords.txt", "w")
#md5 hash the guess and compare against list
def checkHash( pwdGuess ):
    m = hashlib.md5()
    m.update(pwdGuess)
    hashString = m.hexdigest()
    if hashString in hashDict:
        print ("Password found: " + pwdGuess)
        solutionFile.write(hashDict[hashString] + ":\t " + pwdGuess + "\n")

#loop over every possible 5 letter combination
#print if a password is found
for l1 in ascii_lowercase:
    for l2 in ascii_lowercase:
        for l3 in ascii_lowercase:
            for l4 in ascii_lowercase:
                for l5 in ascii_lowercase:
                    checkHash (l1 + l2 + l3 + l4 + l5)

solutionFile.close()
