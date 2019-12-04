import select
import socket
import struct
import sys


srv_ip = sys.argv[1]
srv_port = int(sys.argv[2])

ipv4 = socket.AF_INET
ipv6 = socket.AF_INET6

tcp = socket.SOCK_STREAM
udp = socket.SOCK_DGRAM

server_address = (srv_ip, srv_port)
server = socket.socket(ipv4, udp)
server.settimeout(1.0)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(server_address)

inputs = [server]

packer = struct.Struct('10s 20s')

idoAdatok = {"15":"clear","16":"cloudy","17":"fog"}
varosAdatok = {"Budapest":"clear","Berlin":"cloudy","Becs":"fog","Amsterdam":"rain","London":"heavy rain"}

while inputs:
    timeout = 1
    read, write, excp = select.select(inputs, inputs, inputs, timeout)

    if not(read or write or excp):
        continue

    for s in read:
        try:
            if s is server:
                client, client_addr = s.accept()
                client.setblocking(1)
                inputs.append(client)
            else:
                data = s.recv(packer.size)
                if data:
                    unpacked_data = packer.unpack(data)
                    cmd = unpacked_data[0].decode().strip("\x00")
                    param = unpacked_data[1].decode().strip("\x00")

                    answer = ""

                    if(cmd == "ido"):
                        idoData = idoAdatok.get(param)
                        if idoData == None:
                            answer = "Nincs informacio".encode()
                        else:
                            answer = idoData.encode()
                    elif(cmd == "varos"):
                        varosData = varosAdatok.get(param)
                        if varosData == None:
                            answer = "Nincs informacio".encode()
                        else:
                            answer = varosData.encode()
                    else:
                        answer = "Hibas keres".encode()
                    s.send(answer)
        except socket.error as e:
            print("hiba", e)
            inputs.remove(s)
            if s in write:
                write.remove(s)
            s.close()