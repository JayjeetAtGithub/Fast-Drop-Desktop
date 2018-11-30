#!/usr/bin/vnv python3

import netifaces as ni
import socket
import subprocess
import os
import http.server
import socketserver


def create_hotspot():
    """
    Creates a WiFi hotspot
    """
    return subprocess.run(["nmcli device wifi hotspot con-name %s ssid %s band bg password %s" %
                           ("my-hotspot", "my-hotspot", "hornykhana")], shell=True).returncode


def run(PORT=8000, path="/"):
    """
    Starts the hotspot and starts a local server on port 8000
    """
    create_hotspot()
    print('Connect to %s' % get_hotspot_ip())
    try:
        server(PORT)
    except KeyboardInterrupt:
        deactivate_hotspot()


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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((str(get_hotspot_ip()), PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                print(str(data))


if __name__ == "__main__":
    run()
