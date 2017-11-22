#!/usr/bin/python3

import sys
import os

def xor_file(xored_file, xor_key, output_file):

    b = bytearray(open(xored_file, 'rb').read())

    for i in range(len(b)):
        b[i] ^= int(xor_key, 16)
    open(output_file, 'wb').write(b)

    return

if len(sys.argv) < 2:
	print("Give me something to eat")
	exit(-1)

bup_file = sys.argv[1]
unbup_path = bup_file.split('.')[0]

if not os.path.exists(unbup_path):
    os.makedirs(unbup_path)

os.system( '7z e '+ bup_file + ' -o'+unbup_path)

xor_file(unbup_path + "/Details", "0x6a", unbup_path + "/Details.xor")
xor_file(unbup_path + "/File_0", "0x6a", unbup_path + "/File_0.xor")

print("END: all files are in: " + unbup_path)


