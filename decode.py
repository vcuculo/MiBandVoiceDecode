import opuslib.api.decoder as decoder

dec = decoder.create_state(16000, 1)

#inputfile = 'Log 2020-04-13 21_32_21.txt'
inputfile  = 'capvoice.txt'
outputfile = 'test.pcm'

data = bytearray()
with open(inputfile,'r') as fr:
    print("Reading file %s..." % inputfile)
    for ln in fr:
        if ln.startswith("[Read]20"):
            str_pkt = ln[11:].strip()
        #if ln.startswith("20"):
        #    str_pkt = ln[5:].strip()
            data += bytes.fromhex(str_pkt)

fr.close()

chunk_len = 640
index = 0
output = bytearray()
encodeLength = 0

while (index < len(data)-encodeLength):
    encodeLength = data[index]
    encodeData = data[index+1:index+encodeLength+1]
    decodeData = decoder.decode(dec, bytes(encodeData), len(encodeData), chunk_len, 0);
    output.extend(decodeData[:chunk_len])
    del data[index]
    index += encodeLength;

with open(outputfile, 'wb') as fw:
    fw.write(output)
    print('Saved file %s!\n- 16bit, 16000Hz, 1 channel' % outputfile)

fw.close()

