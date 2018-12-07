import socket
import subprocess
import os
import platform
import argparse
import pyqrcode
import netifaces


class Colors:
    """Color definations
    """
    OK = '\033[92m[+]\033[0m'
    INFO = '\033[93m[!]\033[0m'
    BAD = '\033[91m[-]\033[0m'


def render_qr_code(addr):
    """Generates a QR Code for the IP address and displays it on the terminal
    """
    url = pyqrcode.create(str(addr))
    url.svg("addr.svg", scale=8)
    url.eps("addr.eps", scale=2)
    print(url.terminal(quiet_zone=1))


def get_ip_address(ifname):
    """Returns the ip address of the interface requested
    """
    return netifaces.ifaddresses(ifname)[netifaces.AF_INET][0]['addr']


def create_downloads_folder():
    """Creats a folder named `downloads` if not exists
    """
    if not os.path.exists("downloads"):
        os.mkdir("downloads")


def human(data):
    """
    Decodes byte string into human readable format
    """
    return data.decode("utf-8")


def run(PORT=9000):
    """
    Opens up a socket connection on the port requested
    """
    try:
        print('{} Connect to {}:{}\n\n'.format(
            Colors.OK, get_hotspot_ip(), PORT))
        print('Scan the QR Code from mobile to connect')
        render_qr_code("{}:{}".format(get_hotspot_ip(), PORT))
        server(PORT)
    except KeyboardInterrupt:
        print("{} Server stopped..".format(Colors.BAD))


def get_hotspot_ip():
    """
    Gets the ip address of the hotspot
    """
    return get_ip_address("wlp3s0")


def server(PORT=8000):
    """
    Starts a socket server and waits to get connection and recieve files
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((str(get_hotspot_ip()), PORT))
        s.listen(1)
    except OSError:
        s.close()
    conn, addr = s.accept()
    print("{} Connected by {} ".format(Colors.INFO, addr))
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
    print("{} File {} recieved successfully".format(Colors.INFO, filename))


if __name__ == "__main__":

    art = """
                     ____ ___   ____ 
        ____  __  __/ __ \__ \ / __ )
       / __ \/ / / / /_/ /_/ // /_/ /
      / /_/ / /_/ / ____/ __// ____/ 
     / .___/\__, /_/   /____/_/      
    /_/    /____/                    


    """
    print("\033[93m {}\033[00m" .format(art))
    create_downloads_folder()
    parser = argparse.ArgumentParser()
    parser.add_argument("-p")
    args = parser.parse_args()
    if args.p != None:
        run(int(args.p))
    else:
        run()

