import socket
from input_timeout import readInput
import sys

username = sys.argv[1]

def prompt(n1):
    if n1:
        print("")
    print("<"+username+">")

server_address = ('localhost',10000)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(server_address)
client.sendall(username.encode())
client.settimeout(1.0)

prompt(False)

while True:
    try:
        data = client.recv(200)
        if not data:
            print("Server error")
            sys.exit()
        else:
            print(data.decode())
            sys.stdout.flush()
            prompt(False)
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
        msg = readInput()
        if msg != "":
            msg = msg.strip()
            client.sendall(("["+username+"]").encode())
            prompt(True)
    except socket.timeout:
        pass
    except socket.error as m:
        print("hiba", m)
        client.close()
        break