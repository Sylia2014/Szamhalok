import socket
import struct

server_address=('localhost', 10000)  
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

packer = struct.Struct('I I 1s')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

szam1 = input("Kerem a szamot:")
op = input("Kerem az operatort:")
szam2 = input("Kerem szam2:")
inputs = (int(szam1), int(szam2), op.encode())
packed_data = packer.pack(*inputs)

client.connect(server_address)
client.sendall(packed_data)

data = client.recv(20).decode()
print("Eredmeny: ", data)

client.close()