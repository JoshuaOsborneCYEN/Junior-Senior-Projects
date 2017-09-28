import getopt
import sys

args = str(sys.argv[1:])
print args
optlist, args = getopt.getopt(args, 'd:e')

print optlist
print args
