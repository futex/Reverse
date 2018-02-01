auto file, fname, i, address, size, x;
address = 0x00970000;
size = 0x2E000;
fname = "C:\\Users\\admin\\Desktop\\dump.bin";
file = fopen(fname, "wb");
for (i=0; i<size; i++, address++)
{
 x = DbgByte(address);
 fputc(x, file);
}
fclose(file);