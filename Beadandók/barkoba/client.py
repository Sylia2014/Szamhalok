import socket
import sys

server_address = (sys.argv[1], sys.argv[2])
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(server_address)
client.settimeout(1.0)