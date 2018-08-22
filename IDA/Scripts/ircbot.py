#For ircbot malware sample: d9b2e9d8826cab35e3287a0a35248f40
#PS: Exe the sample after the xor key creation

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

decrypt_function = Appcall.proto(FUNC_NAME, PROTO)

decrypt(decrypt_function)

print("Done")