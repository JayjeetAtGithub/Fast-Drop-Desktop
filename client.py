# pyP2P Desktop Client

import socket
import argparse
import sys


def send():
    """
    Send the file in byte chunks to the server
    """
    filename = str(input("Enter file path :"))
    f = open(filename, 'rb')
    l = f.read(1024)
    while l:
        s.send(l)
        l = f.read(1024)
    print("File sent successfully")
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-host")
    parser.add_argument("-p")
    args = parser.parse_args()
    s = socket.socket()
    if args.host != None and args.p != None:
        host = str(args.host)
        port = int(args.p)
        s.connect((host, port))
        try:
            send()
        except KeyboardInterrupt:
            print("Aborting...")
    else:
        print("Host/Port not provided")
        sys.exit(0)
