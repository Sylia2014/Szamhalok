import socket
import sys

server_address = (sys.argv[1], int(sys.argv[2]))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(server_address)
client.settimeout(1.0)


while True:
    try:
        answer = client.recv(1024)
        if not answer:
            print("Server error")
            sys.exit()
        else:
            print(answer.decode())
            sys.stdout.flush()
    except SystemExit as m:
        client.close()
        break
    except socket.timeout:
        pass
    except socket.error as e:
        print("hiba", e)
        client.close()
        break

""""
Keresés(N,X,Y,VAN,SORSZ):
  E:=1; U:=N
  Ciklus
    K:=[(E+U)/2]                 [E+U felének egész értéke]
    Elágazás
      Y<X[K] esetén U:=K-1
      Y>X[K] esetén E:=K+1
    Elágazás vége
  amíg E≤U és X[K]?Y
  Ciklus vége
  VAN:=(E≤U)
  Ha VAN akkor SORSZ:=K
Eljárás vége.
"""

# def logarithmicSearch():
#     start = 1
#     end = 100
#
#     while True:
#         stuff()
#         if not condition():
#             break