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
import select

srv_ip = sys.argv[1]
srv_port = int(sys.argv[2])
answer_ok = "OK"

server_address = (srv_ip, srv_port)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(1.0)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(server_address)
server.listen(5)

class Checksum:
    # BE|<fájl azon.>|<érvényesség másodpercben>|<checksum hossza bájtszámban>|<checksum bájtjai>
    def __init__(self, fajl_azon, ervenyesseg, hossz, bajtok):
        self.fajl_azon = fajl_azon
        self.ervenyesseg = ervenyesseg
        self.hossz = hossz
        self.bajtok = bajtok

    @property
    def fajl_azon(self):
        return self._fajl_azon

    @property
    def hossz(self):
        return self._hossz

    @property
    def bajtok(self):
        return self._bajtok

    @property
    def ervenyesseg(self):
        return self._ervenyesseg

    @ervenyesseg.setter
    def ervenyesseg(self, value):
        self._ervenyesseg = value

    @fajl_azon.setter
    def fajl_azon(self, value):
        self._fajl_azon = value

    @hossz.setter
    def hossz(self, value):
        self._hossz = value

    @bajtok.setter
    def bajtok(self, value):
        self._bajtok = value

    #megírni valahogy az érvénytelen fájlok törlését
#     whileba végig kell menni a checksumok tömbön, és mikor felveszem akkor letárolom hogy mikor vettem fel, és ha lejárt akkor törlés


inputs = [server]
checksumok = []


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
                data = s.recv(1024)
                if data:
                    splitted_data = data.decode().split("|")
                    if splitted_data[0] == "BE":
                        print(data)
                        # BE|<fájl azon.>|<érvényesség másodpercben>|<checksum hossza bájtszámban>|<checksum bájtjai>
                        checksum = Checksum(splitted_data[1], splitted_data[2], splitted_data[3], splitted_data[4])
                        checksumok.append(checksum)
                        s.send(answer_ok.encode())
                    elif splitted_data[0] == "KI":
                        print(data)
                        for checksum in checksumok:
                            if(checksum.fajl_azon == splitted_data[1]):
                                # <checksum hossza bájtszámban>|<checksum bájtjai>
                                # Ha nincs checksum, akkor ezt küldi: 0|
                                if(checksum.hossz == 0):
                                    s.send("0|".encode())
                                else:
                                    checksum_msg = checksum.hossz + "|" + checksum.bajtok
                                    s.send(checksum_msg.encode())
                else:
                    inputs.remove(s)
        except socket.error as e:
            print("hiba", e)
            inputs.remove(s)
            if s in write:
                write.remove(s)
            s.close()