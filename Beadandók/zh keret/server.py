import select
import socket
import sys

srv_ip = sys.argv[1]
srv_port = int(sys.argv[2])

ipv4 = socket.AF_INET
ipv6 = socket.AF_INET6

tcp = socket.SOCK_STREAM
udp = socket.SOCK_DGRAM

server_address = (srv_ip, srv_port)
server = socket.socket(ipv4, tcp)
server.settimeout(1.0)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(server_address)
server.listen(5)

inputs = [server]  #bemeneti csatornák, ha több van, pl mint a netcopynál, akkor azt is fel kell ide venni

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
                data = s.recv(1024)  #
                if data:
                    print(data.decode())
                    #többi logika
        except socket.error as e:
            print("hiba", e)
            inputs.remove(s)
            if s in write:
                write.remove(s)
            s.close()