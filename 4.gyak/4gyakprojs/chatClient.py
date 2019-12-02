import socket
import sys
from input_timeout import readInput

username = sys.argv[1]


def prompt(nl):
    if nl:
        print("")
    print("<" + username + ">")


server_address = ("localhost", 10000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(server_address)
client.sendall(username.encode())
client.settimeout(1.0)
prompt(False)

while True:
    try:
        data = client.recv(200)
        if not data:
            print("Server down")
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
        print("hiba", e)
        break

    try:
        msg = readInput()
        msg = msg.strip()
        if (msg != ""):
            client.sendall(("[" + username + "]" + msg).encode())
            prompt(True)
    except socket.timeout:
        pass
    except socket.error as e:
        print(e)
        break