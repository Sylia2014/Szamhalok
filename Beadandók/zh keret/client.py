import socket
import sys

srv_ip = sys.argv[1]
srv_port = int(sys.argv[2])

ipv4 = socket.AF_INET
ipv6 = socket.AF_INET6

tcp = socket.SOCK_STREAM
udp = socket.SOCK_DGRAM

server_address = (srv_ip, srv_port)
client = socket.socket(ipv4, socket.SOCK_STREAM)

client.connect(server_address)

while True:
    try:
        data = client.recv(200)
        if not data:
            print("Server error")
            sys.exit()
        else:
            print(data.decode())
            #többi logika
    except SystemExit as m:
        client.close()
        break
    except socket.timeout:
        pass
    except socket.error as e:
        print("hiba",e)
        client.close()
        break

    try:
        msg = input("prompt") #beolvasás konzolról
        # lehet bármi más is
        if msg != "":
            msg = msg.strip()
            client.send(msg.encode())
    except socket.timeout:
        pass
    except socket.error as m:
        print("hiba", m)
        client.close()
        break