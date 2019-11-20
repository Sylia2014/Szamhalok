"""
• Működés:
    – Bindolja a socketet a parancssori argumentumban megadott címre.
    – Vár egy kliensre.
    – Ha acceptálta, akkor fogadja a fájl bájtjait sorfolytonosan és kiírja a paracssori argumentumban megadott fájlba.
    – Fájlvége jel olvasása esetén lezárja a kapcsolatot és utána ellenőrzi a fájlt a Checksum szerverrel.
    – A Checksum szerverrel az ott leírt módon kommunikál.
    – Hiba esetén a stdout-ra ki kell írni: CSUM CORRUPTED
    – Helyes átvitel esetén az stdout-ra ki kell írni: CSUM OK
    – Fájl fogadása és ellenőrzése után terminál a program.
• Futtatás:
    – .\netcopy_srv.py <srv_ip> <srv_port> <chsum_srv_ip> <chsum_srv_port> <fájl azon> <fájlnév elérési úttal>
        • <fájl azon>: egész szám ua. mint a kliensnél – ez alapján kéri le a szervertől a checksumot
        • <srv_ip> <srv_port>: a netcopy szerver elérhetősége – bindolásnál kell
        • <chsum_srv_ip> <chsum_srv_port>: a Checksum szerver elérhetősége
        • <fájlnév> : ide írja a kapott bájtokat
"""
import hashlib
import select
import socket
import sys

srv_ip = sys.argv[1]
srv_port = int(sys.argv[2])
chsum_srv_ip = sys.argv[3]
chsum_srv_port = int(sys.argv[4])
fajl_azon = sys.argv[5]
fajl_eleresi_ut = sys.argv[6]

server_address = (srv_ip, srv_port)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(1.0)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(server_address)
server.listen(5)

checksum_server_address = (chsum_srv_ip, chsum_srv_port)
checksum_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    checksum_client.connect(checksum_server_address)
except socket.error as e:
    checksum_client.close()

inputs = [server, checksum_client]
kapott = []
mentett = []

eredm_file = open(fajl_eleresi_ut, "wb")
m = hashlib.md5()

while server.fileno() != -1:
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
                data = s.recv(1024)
                if data:
                    if(s is checksum_client):
                        splitted_data = data.decode().split("|")
                        # print(splitted_data)

                        # print("file try to open")
                        with open(fajl_eleresi_ut, 'rb') as file:
                            for byte in iter(lambda: file.read(1), b''):
                                mentett.append(byte)
                                # print(mentett)
                                m.update(byte)
                        vege = "[" + str(len(m.hexdigest())) + ", " + m.hexdigest() + "]"
                        # print(vege)

                        # for i in range(len(mentett)):
                            # print(str(mentett[i]) + " " + str(kapott[i]))

                        if int(splitted_data[0]) != len(m.hexdigest()) or splitted_data[1] != m.hexdigest():
                            print("CSUM CORRUPTED")
                        else:
                            print("CSUM OK")
                        server.close()
                    else:
                        kapott.append(data)
                        # print(kapott)
                        eredm_file.write(data)
                        m.update(data)
                else:
                    eredm_file.flush()
                    s.close()
                    inputs.remove(s)
                    eredm_file.close()
                    # print("file closed")
                    if s in write:
                        checksum_msg = "KI|" + fajl_azon
                        checksum_client.send(checksum_msg.encode())

        except socket.error as e:
            print("hiba", e)
            inputs.remove(s)
            if s in write:
                write.remove(s)
            s.close()