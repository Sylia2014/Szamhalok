import socket
import sys
import queue
import random
import select

server_address = (sys.argv[1], int(sys.argv[2]))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(1.0)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

server.bind(server_address)
server.listen(5)

randNumber = random.randint(1, 100)

inputs = [server]
msg_q = queue.Queue()

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
                tip = client.recv(1024).decode().strip()
                operator = tip.split(",")[0]
                number = tip.split(",")[1]
                print("Tipp: ", tip, client_addr)
                inputs.append(client)

                if operator == "<":
                    if randNumber < number:
                        msg_q.put("I")
                    else:
                        msg_q.put("N")
                elif operator == ">":
                    if randNumber > number:
                        msg_q.put("I")
                    else:
                        msg_q.put("N")
                elif operator == "=":
                    if randNumber == number:
                        msg_q.put("Y")
                    else:
                        msg_q.put("V")
            else:
                data = s.recv(1024).strip()
                if data:
                    msg_q.put(data)
                # else:
                #     print("Kilepett: ", username[s])
                #     msg_q.put("["+name+"] is LOGOUT")
                #
                #     inputs.remove(s)
                #     if s in write:
                #         write.remove(s)
                #     s.close()
        except socket.error as e:
            print("hiba", e)
            inputs.remove(s)
            if s in write:
                write.remove(s)
            s.close()