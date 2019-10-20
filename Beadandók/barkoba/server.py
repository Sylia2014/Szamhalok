import socket
import sys
import queue
import random
import select
import struct

server_address = (sys.argv[1], int(sys.argv[2]))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(1.0)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

server.bind(server_address)
server.listen(5)

YES = "I".encode()
NO = "N".encode()
WIN = "Y".encode()
LOSE = "K".encode()
GAME_OVER = "V".encode()
packer = struct.Struct('1s I')

randNumber = random.randint(1, 100)
print(randNumber)

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
                inputs.append(client)
            else:
                data = s.recv(packer.size)
                if data:
                    unpacked_data = packer.unpack(data)
                    print(unpacked_data[0].decode(), unpacked_data[1])
                    operator = unpacked_data[0].decode()
                    number = unpacked_data[1]

                    random_ans_num = random.randint(1,100)
                    if operator == "<":
                        if randNumber < number:
                            answer = (YES, random_ans_num)
                            packed_data = packer.pack(*answer)
                            s.send(packed_data)
                        else:
                            answer = (NO, random_ans_num)
                            packed_data = packer.pack(*answer)
                            s.send(packed_data)
                    elif operator == ">":
                        if randNumber > number:
                            answer = (YES, random_ans_num)
                            packed_data = packer.pack(*answer)
                            s.send(packed_data)
                        else:
                            answer = (NO, random_ans_num)
                            packed_data = packer.pack(*answer)
                            s.send(packed_data)
                    elif operator == "=":
                        if randNumber == number:
                            answer = (WIN, random_ans_num)
                            packed_data = packer.pack(*answer)
                            s.send(packed_data)
                            inputs.remove(s)
                            if s in write:
                                write.remove(s)
                            s.close()
                            game_over_msg = (GAME_OVER, random_ans_num)
                            game_over_data = packer.pack(*game_over_msg)
                            for c in write:
                                c.send(game_over_data)
                            # s.send(packed_data)
                        else:
                            answer = (LOSE, random_ans_num)
                            packed_data = packer.pack(*answer)
                            s.send(packed_data)
                            inputs.remove(s)
        except socket.error as e:
            print("hiba", e)
            inputs.remove(s)
            if s in write:
                write.remove(s)
            s.close()