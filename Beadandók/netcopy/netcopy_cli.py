"""
• Működés:
    – Csatlakozik a szerverhez, aminek a címét és portját parancssori argumentumban kapja meg.
    – Fájl bájtjainak sorfolytonos átvitele a szervernek.
    – A Checksum szerverrel az ott leírt módon kommunikál.
    – A fájl átvitele és a checksum elhelyezése után bontja a kapcsolatot és terminál.
• Futtatás:
    – .\netcopy_cli.py <srv_ip> <srv_port> <chsum_srv_ip> <chsum_srv_port> <fájl azon> <fájlnév elérési úttal>
        • <fájl azon>: egész szám
        • <srv_ip> <srv_port>: a netcopy szerver elérhetősége
        • <chsum_srv_ip> <chsum_srv_port>: a Checksum szerver elérhetősége
"""
import socket
import sys
import hashlib

srv_ip = sys.argv[1]
srv_port = int(sys.argv[2])
chsum_srv_ip = sys.argv[3]
chsum_srv_port = int(sys.argv[4])
fajl_azon = sys.argv[5]
fajl_eleresi_ut = sys.argv[6]

netcopy_server_address = (srv_ip, srv_port)
netcopy_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

checksum_server_address = (chsum_srv_ip, chsum_srv_port)
checksum_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
answer = ''

try:
    netcopy_client.connect(netcopy_server_address)
    checksum_client.connect(checksum_server_address)
except socket.error as e:
    netcopy_client.close()
    checksum_client.close()

m = hashlib.md5()

with open(fajl_eleresi_ut, 'rb') as file:
    for byte in iter(lambda: file.read(1), b''):
        netcopy_client.send(byte)
        m.update(byte)

# BE|<fájl azon.>|<érvényesség másodpercben>|<checksum hossza bájtszámban>|<checksum bájtjai>
checksum_msg = "BE|" + fajl_azon + "|" + str(60) + "|" + str(len(m.hexdigest())) + "|" + m.hexdigest()
checksum_client.send(checksum_msg.encode())
try:
    answer = checksum_client.recv(1024)
    if not answer:
        print("Server error")
        sys.exit()
    else:
        print(answer.decode())
except SystemExit as m:
    netcopy_client.close()
    checksum_client.close()
except socket.timeout:
    pass
except socket.error as e:
    print("hiba", e)
    netcopy_client.close()
    checksum_client.close()

netcopy_client.close()
checksum_client.close()