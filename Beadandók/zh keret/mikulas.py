import socket
import sys
import struct
import time

utvonal_srv_ip = sys.argv[1]
utvonal_srv_port = int(sys.argv[2])

idojaras_srv_ip = sys.argv[3]
idojaras_srv_port = int(sys.argv[4])
szint = int(sys.argv[5])

ipv4 = socket.AF_INET
ipv6 = socket.AF_INET6

tcp = socket.SOCK_STREAM
udp = socket.SOCK_DGRAM

utvonal_server_address = (utvonal_srv_ip, utvonal_srv_port)
utvonal_client = socket.socket(ipv4, tcp)
utvonal_client.connect(utvonal_server_address)

idojaras_server_address = (idojaras_srv_ip, idojaras_srv_port)
idojaras_client = socket.socket(ipv4, udp)
idojaras_client.connect(idojaras_server_address)

packer = struct.Struct('10s 20s')

cmd = 'ido'.encode()
param = '17'.encode()

data = (cmd, param)
packed_data = packer.pack(*data)

if szint == 2:
    utvonal_client.send(packed_data)
elif szint == 3:
    idojaras_client.send(packed_data)
elif szint == 4:
    time.sleep(2)
    utvonal_client.send(packed_data)

try:
    data = utvonal_client.recv(200)
    if not data:
        print("Server error")
        sys.exit()
    else:
        print(data.decode())
        #többi logika

except SystemExit as m:
    utvonal_client.close()
    idojaras_client.close()
except socket.timeout:
    pass
except socket.error as e:
    print("hiba",e)
    utvonal_client.close()
    idojaras_client.close()