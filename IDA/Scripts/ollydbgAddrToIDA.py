from idaapi import * 
import idautils
import idc

#https://hooked-on-mnemonics.blogspot.ch/2012/09/importing-ollydbg-addresses-into-ida.html

class OLLYDBG_ADDR_TO_IDA:
    def __init__(self):
        self.fileName = AskFile(0, "*.*", 'Ollydbg Address Exported')
        self.content = []
        self.getFile()
        self.renameAddr()

    def getFile(self):
        try:
            self.content = open(self.fileName, 'r').readlines()
        except:
            return 
    
    def renameAddr(self):
        for addr in self.content:
            list_addr_name = addr.split()
            if len(list_addr_name) != 3: 
                continue
            api_addr = int(list_addr_name[0],16)
            api_name = list_addr_name[2].split('.')[1]
            MakeNameEx(api_addr, api_name, SN_NOWARN)

OLLYDBG_ADDR_TO_IDA()
