# pyP2P Desktop Client

import socket

s = socket.socket()
host = "10.42.0.1"
port = 9000
s.connect((host, port))

filename = str(input("Enter filename : "))


def send():
    f = open(filename, 'rb')
    l = f.read(1024)
    while l:
        s.send(l)
        l = f.read(1024)
    print("File sent successfully")
    f.close()


if __name__ == "__main__":
    send()
