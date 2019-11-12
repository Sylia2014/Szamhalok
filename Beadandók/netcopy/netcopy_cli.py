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

netcopy_server_address = (sys.argv[1], int(sys.argv[2]))
netcopy_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

checksum_server_address = (sys.argv[3], int(sys.argv[4]))
checksum_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

netcopy_client.connect(netcopy_server_address)
checksum_client.connect(checksum_server_address)