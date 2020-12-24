import camellia
import zlib

#read pcap bytes
with open('poisonIvy.pcap', 'rb') as fileInput:
    pcap = fileInput.read()

#look for the 5byte identifier - NdH16 in our case
#skip first two packets
begin = pcap.find('NdH16'.encode('latin-1'))
end = pcap.find('\x00\x00\x00\x00\x00\x00\x00\x00'.encode('latin-1'), begin)
begin = pcap.find('NdH16'.encode('latin-1'), end)
end = pcap.find('\x00\x00\x00\x00\x00\x00\x00\x00'.encode('latin-1'), begin)

#get the 3rd packet data start and end
begin = pcap.find('NdH16'.encode('latin-1'), end)
end = pcap.find('\x00\x00\x00\x00\x00\x00\x00\x00'.encode('latin-1'), begin)

#extract packet data and decompress it
data = pcap[begin:end]
data = zlib.decompress(data[15:])
#skip first byte
data = data[1:len(data)]

#add padding to the key to fill 32bytes
masterKey = 'casper' + "\x00"*(32-len('casper'))
camelliaCipher = camellia.CamelliaCipher(key=masterKey.encode(), mode=camellia.MODE_ECB)
decrypted = camelliaCipher.decrypt(data + ("\x00"*(32-len(data))).encode()  )

print(decrypted)
