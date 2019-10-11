import socket
import sys
import queue

server_address = (sys.argv[1], int(sys.argv[2]))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(1.0)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

server.bind(server_address)
server.listen(5)

inputs = [server]
msq_q = queue.Queue()

while inputs:
    timeout = 1