"""
• Beszúr üzenet
    – Formátum: szöveges
    – Felépítése: BE|<fájl azon.>|<érvényesség másodpercben>|<checksum hossza bájtszámban>|<checksum bájtjai>
    – A „|” delimiter karakter
    – Példa: BE|1237671|60|12|abcdefabcdef
        • Ez esetben: a fájlazon: 1237671, 60mp az érvényességi idő, 12 bájt a checksum, abcdefabcdef maga a checksum
    – Válasz üzenet: OK
• Kivesz üzenet
    – Formátum: szöveges
    – Felépítése: KI|<fájl azon.>
    – A „|” delimiter karakter
    – Példa: KI|1237671
        • Azaz kérjük az 1237671 fájl azonosítóhoz tartozó checksum-ot
    – Válasz üzenet: <checksum hossza bájtszámban>|<checksum bájtjai>
        • Példa: 12|abcdefabcdef
    – Ha nincs checksum, akkor ezt küldi: 0|
• Futtatás
    – .\checksum_srv.py <ip> <port>
        • <ip> - pl. localhost a szerver címe bindolásnál
        • <port> - ezen a porton lesz elérhető
    – A szerver végtelen ciklusban fut és egyszerre több klienst is ki tud szolgálni. A kommunikáció TCP, csak a fenti üzeneteket kezeli.
    – Lejárat utáni checksumok törlődnek.
"""

import socket
import sys

server_address = (sys.argv[1], int(sys.argv[2]))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(1.0)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(server_address)
server.listen(5)