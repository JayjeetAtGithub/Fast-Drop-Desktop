#!/usr/bin/vnv python3

# pyP2P Desktop Server

import netifaces as ni
import socket
import subprocess
import os
import http.server
import socketserver
import platform


def human(data):
    return data.decode("utf-8")


def create_hotspot():
    """
    Creates a WiFi hotspot
    """
    if platform.system() == 'Linux':
        os.system("nmcli device wifi hotspot con-name %s ssid %s band bg password %s" %
                  ("my-hotspot", "my-hotspot", "hornykhana"))


def run(PORT=9000, path="/"):
    """
    Starts the hotspot and starts a local server on port 8000
    """

    # Hotspot to be turned on only when argument passed
    # create_hotspot()
    print('Connect to %s' % get_hotspot_ip())
    try:
        server(PORT)
    except KeyboardInterrupt:
        pass


def get_hotspot_ip():
    """
    Gets the ip address at which the hotspot is started
    """
    return ni.ifaddresses('wlp3s0')[ni.AF_INET][0]['addr']


def deactivate_hotspot():
    """
    Closes the hotspot
    """
    os.system("nmcli connection down my-hotspot")


def server(PORT):
    """
    Starts a socket server and waits to get connections and recieve files
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((str(get_hotspot_ip()), PORT))
            s.listen(1)
        except OSError:
            s.close()
            deactivate_hotspot()
        conn, addr = s.accept()
        print('Connected by', addr)
        for i in range(100):
            receive_file(conn, i)


def receive_file(conn, i):
    """
    Recieves  a file byte by byte
    """
    filename = "recieved_{}.txt".format(i)
    f = open(filename, 'w')
    print("Receiving file {}...".format(i))
    while True:
        data = conn.recv(1024)
        print(human(data))
        if human(data) == "close":
            break
        f.write(human(data))
    f.close()
    print("File {} recieved successfully".format(i))


if __name__ == "__main__":
    run()
