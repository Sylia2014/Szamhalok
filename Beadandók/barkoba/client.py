import random
import socket
import sys
import struct
import math
import time

print(sys.argv[1])
server_address = (sys.argv[1], int(sys.argv[2]))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(server_address)
packer = struct.Struct('1s I')

res = ''

lower_limit = 1
upper_limit = 100
tip = 50
operator = '<'.encode()


def logarithmical_search(answ, prev_tip, low_lim, upp_lim):
    global lower_limit
    global upper_limit
    global tip
    global operator

    if (low_lim == prev_tip or upp_lim == prev_tip) and answ == 'N':
        tip = prev_tip
        operator = "=".encode()
        return tip
    if answ == 'N':
        lower_limit = prev_tip
        tip = math.floor((prev_tip + upp_lim) / 2)
        return tip
    elif answ == 'I':
        upper_limit = prev_tip
        tip = math.floor((prev_tip + low_lim) / 2)
        return tip


data = (operator, tip)
packed_data = packer.pack(*data)
client.send(packed_data)

while res != 'Y' or res != 'V' or res != 'K':
    try:
        answer = client.recv(70)
        if not answer:
            print("Server error")
            sys.exit()
        else:
            unpacked_data = packer.unpack(answer)
            print(unpacked_data[0].decode(), unpacked_data[1])
            res = unpacked_data[0].decode()

            if res == 'Y' or res == 'V' or res == 'K':
                break

            next_tip = logarithmical_search(res, tip, lower_limit, upper_limit)

            data = (operator, next_tip)
            packed_data = packer.pack(*data)
            time.sleep(random.randint(1,5))
            client.send(packed_data)
    except SystemExit as m:
        client.close()
        break
    except socket.timeout:
        pass
    except socket.error as e:
        print("hiba", e)
        client.close()
        break

client.close()
