#!/usr/bin/env python

import subprocess
import os

for i in range(1, 30):
	for j in range(1, 8):
		os.system("./steg.py -r -b -w stars7.bmp -o " + str(100*i) + " -i " + str(10*j))
