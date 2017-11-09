#!/usr/bin/python

import sys
import io

"""

    Extract PE file from a Kaspersky quarantine file.
    The output file need to be cleaned manually, there is still some headers bytes inside

  ----------------------------------------------------------------------------
  "THE BEER-WARE LICENSE" (Revision 42):
  @futex90 wrote this file.  As long as you retain this notice you
  can do whatever you want with this stuff. If we meet some day, and you think
  this stuff is worth it, you can buy me a beer in return.   
  ----------------------------------------------------------------------------

"""

 if len(sys.argv) != 3:
    print ("Usage: %s [kaspersky (.klq) file] [output file]" % __file__)
	sys.exit(1)

f = open(sys.argv[1])
buff=""

key =[0xE2,0x45,0x48,0xEC,0x69,0x0E,0x5C,0xAC]

i = 0

for car in f.read():

   buff += chr((ord(car) ^ key[i % len(key)] ))
   i += 1


foutput=open(sys.argv[1],'w+')
foutput.write(buff)
foutput.close()
