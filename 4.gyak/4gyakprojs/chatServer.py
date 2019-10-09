import socket
import select
import Queue as queue

server_address = ('', 10000)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(1.0)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

server.bind(server_address)
server.listen(5)

inputs = [server]
msg_q = queue.Queue()
username = {}

while inputs:
    timeout = 1
    read, write, excp = select.select(inputs,inputs,inputs, timeout)

    if not(read or write or excp):
        continue

    for s in read:
        try:
            if s is server:
                client, client_addr = s.accept()
                client.setblocking(1)
                name = client.recv(20).decode().strip()
                print("Csatlakozott: ", name, client_addr)
                username[client] = name
                inputs.append(client)
                msg_q.put("["+name+"] is LOGIN")
            else:
                data = s.recv(200).strip()
                if data:
                    msg_q.put(data)
                else:
                    print("Kilepett: ", username[s])
                    msg_q.put("["+name+"] is LOGOUT")

                    inputs.remove(s)
                    if s in write:
                        write.remove(s)
                    s.close()
        except socket.error as e:
            print("hiba", e)
            inputs.remove(s)
            if s in write:
                write.remove(s)
            s.close()
    while not msg_q.empty():
        try:
            next_msg = msg_q.get_nowait()
            print("msg", next_msg)
        except queue.Empty:
            break
        else:
            for s in write:
                if(username[s] in next_msg):
                    s.sendall(next_msg.encode())
                    print(username[s])
