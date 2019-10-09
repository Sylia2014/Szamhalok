import socket
import struct

server_address = ('', 10000)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(server_address)

server.listen(1)
server.settimeout(1.0)

unpacker = struct.Struct('I I 1s')

while True:
    try:
        client, client_addr = server.accept()
        adat = client.recv(unpacker.size)
        print("kaptam:", adat)
        unpacked_data = unpacker.unpack(adat)

        x = eval(str(unpacked_data[0]) + unpacked_data[2].decode() + str(unpacked_data[1]))
        client.sendall(str(x).encode())

        client.close()
        
    except KeyboardInterrupt:
        break
    except socket.timeout:
        pass
    except socket.error as m:
        print("hiba", m)

server.close()