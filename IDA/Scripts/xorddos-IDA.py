# IDA basic script for uncrypt xored confguration of xorddos linux malware
# By Futex


def strxor(a, b):
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b*100)])

xorkey_addr = idc.LocByName("xorkeys")
crypted_addr = idc.LocByName("unk_80B32EC")
xorkey=GetString(xorkey_addr)

print "xorkey: " + xorkey + " crypted addr: " + hex(crypted_addr)

remotestr = GetString(crypted_addr, 100, 0)

config = strxor(remotestr, xorkey)

print config
