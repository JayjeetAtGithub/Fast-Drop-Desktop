# pyP2P Desktop Server

import socket
import subprocess
import os
import platform
import argparse
import fcntl
import struct


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def human(data):
    """
    Decodes byte string.
    """
    return data.decode("utf-8")


def run(PORT=9000):
    """
    Starts the hotspot and starts a local server on port 8000
    """

    # Hotspot to be turned on only when argument passed
    # create_hotspot()
    print('Connect to {}:{}'.format(get_hotspot_ip(), PORT))
    try:
        server(PORT)
    except KeyboardInterrupt:
        print("Server stopped..")


def get_hotspot_ip():
    """
    Gets the ip address at which the hotspot is started.
    """
    return get_ip_address("wlp3s0")


def server(PORT=8000):
    """
    Starts a socket server and waits to get connections and recieve files
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((str(get_hotspot_ip()), PORT))
        s.listen(1)
    except OSError:
        s.close()
    conn, addr = s.accept()
    print("Connected by {} ".format(addr))
    filename = str(raw_input("Enter filename : "))
    try:
        receive_file(conn, filename)
    except Exception:
        s.close()


def receive_file(conn, filename):
    """
    Recieves  a file byte by byte
    """
    f = open("./downloads/{}".format(filename), 'wb')
    data = conn.recv(1024)
    while data:
        f.write(data)
        data = conn.recv(1024)
    f.close()
    print("File {} recieved successfully".format(filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p")
    args = parser.parse_args()
    if args.p != None:
        run(int(args.p))
    else:
        run()

