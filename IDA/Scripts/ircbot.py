#For ircbot malware sample: d9b2e9d8826cab35e3287a0a35248f40
#PS: Exe the sample after the xor key creation

from idaapi import *
import struct

def convert_little_endian(value):
	return struct.unpack('>I',struct.pack('<I', value))[0]

def patch_bytes(address, bytes):

	tmp_value_value=struct.unpack('>L', bytes)[0]
	new_value=convert_little_endian(tmp_value_value)

	PatchDword(address, new_value)

def patch():

	key = bytearray([0xE0, 0xB2, 0xAA, 0xD9, 0xC0, 0xE5, 0xA4, 0xF9, 0xB5, 0xA6, 0x9C, 0x97, 0xB0, 0xD0, 0x8C, 0x8D])
	address= 0x0040EC10

	patch_bytes(address, key[0:4])
	patch_bytes(address+4, key[4:8])
	patch_bytes(address+8, key[8:12])
	patch_bytes(address+12, key[12:16])

def decrypt(func):
	datastart = SegByBase(SegByName(".data"))
	dataend = SegEnd(datastart)
	print("Start: " + hex(datastart) + ", end: "+ hex(dataend) +"\n")
	print("func:" + str(func))
          
	for i in range(datastart, dataend):
	   name = Name(i)
	   	   
	   if name.startswith("a"):
	       func(i)

	       print("i2:" + hex(i) + ", value: " + GetString(i, -1, ASCSTR_C))
	       MakeComm(i, "Value: " + GetString(i))

#Clean the output	   
form = idaapi.find_tform("Output window")
idaapi.switchto_tform(form, True);
idaapi.process_ui_action("msglist:Clear")          

FUNC_NAME = "XORStringDecrypt" #0x0040216
PROTO = "int __cdecl XORStringDecrypt(char *str);".format(FUNC_NAME)

patch()

decrypt_function = Appcall.proto(FUNC_NAME, PROTO)

decrypt(decrypt_function)

print("Done")