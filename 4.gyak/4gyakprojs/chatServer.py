import socket
import select
import queue

#a futtatásnál ha be akarok olvasni valamit a konzolról akkor emulate terminal in output console
server_address = ('', 10000)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(1.0)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(server_address)

server.listen(5)

inputs = [server]

msg_q = queue.Queue()
username = {}

while inputs:
    timeout = 1
    readable, writeable, exceptable = select.select(inputs, inputs, inputs, timeout)

    if not (readable or writeable or exceptable):
        continue

    for s in readable:
        try:
            if s is server:
                client, client_addr = s.accept()
                client.setblocking(1)
                name = client.recv(20).decode().strip()
                print("Kliens csatlakozott: ", name, client_addr)
                username[client] = name
                inputs.append(client)
                msg_q.put("[" + name + "] is LOGIN")
            else:
                data = s.recv(200).strip()
                if data:
                    msg_q.put(data.decode())
                else:
                    print("Kliens kilepett")
                    msg_q.put("[" + username[s] + "] is LOGOUT")
                    inputs.remove(s)
                    if s in writeable:
                        writeable.remove(s)
                    s.close()
        except socket.error as m:
            print("hiba", m)
            inputs.remove(s)
            if s in writeable:
                writeable.remove(s)
            s.close()

    while not msg_q.empty():
        try:
            next_msg = msg_q.get_nowait()
            print("msg", next_msg)
        except queue.Empty:
            break
        else:
            for s in writeable:
                if not username[s] in next_msg:
                    s.sendall(next_msg.encode())
                    print("Send", username[s])