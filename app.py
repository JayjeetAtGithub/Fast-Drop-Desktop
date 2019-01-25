#############################
##### pyP2P 1.1 (alpha) #####
#############################

import socket
import os
import argparse
import pyqrcode
import netifaces


class Logger:
    """Color definations
    """
    OK = '\033[92m[+]\033[0m'
    INFO = '\033[93m[!]\033[0m'
    ERROR = '\033[91m[-]\033[0m'

    def success(self, message):
        print("{} {}".format(Logger.OK, message))

    def info(self, message):
        print("{} {}".format(Logger.INFO, message))

    def error(self, message):
        print("{} {}".format(Logger.ERROR, message))


logger = Logger()


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
    """Decodes byte string into human readable format
    """
    return data.decode("utf-8")


def run(PORT=9000):
    """Opens up a socket connection on the port requested
    """
    try:
        logger.success('Connect to {}:{}'.format(get_hotspot_ip(), PORT))
        logger.info('Scan the QR Code to connect :)')
        render_qr_code("{}:{}".format(get_hotspot_ip(), PORT))
        handshake(PORT)
    except (KeyboardInterrupt, Exception):
        logger.error("Server stopped !")


def get_hotspot_ip():
    """Gets the ip address of the hotspot
    """
    return get_ip_address("wlp3s0")


def handshake(PORT):
    """Starts a socket server and waits to get connection and recieve files
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((str(get_hotspot_ip()), PORT))
        s.listen(1)
    except OSError:
        s.close()
    while 1:
        conn, addr = s.accept()
        logger.info("Connected by {}".format(addr))
        dec = int(input("Receive or Send ? (1/2) "))
        if dec == 1:
            filename = str(input("Enter file name : "))
            try:
                receive_file(conn, filename)
            except Exception:
                s.close()
        elif dec == 2:
            path = str(input("Enter file path : "))
            try:
                send_file(conn, path)
            except Exception:
                s.close()
        else:
            logger.error("Wrong choice !")


def receive_file(conn, filename):
    """Recieves  a file byte by byte
    """
    f = open("./downloads/{}".format(filename), 'wb')
    data = conn.recv(1024)
    while data:
        f.write(data)
        data = conn.recv(1024)
    f.close()
    logger.success("File received successfully !")


def send_file(conn, filepath):
    """Sends a file over socket
    """
    if os.path.exists(filepath) and os.path.isfile(filepath):
        f = open(filepath, 'rb')
        data = f.read(1024)
        while data:
            conn.send(data)
            data = f.read(1024)
        f.close()
        logger.success("File sent successfully !")
    else:
        logger.error("Invalid file path !")


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
    if args.p is not None:
        run(int(args.p))
    else:
        run()
