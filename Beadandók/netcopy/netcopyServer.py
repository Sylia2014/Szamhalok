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