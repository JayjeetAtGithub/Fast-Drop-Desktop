import socket
import os
import argparse
import pyqrcode
import netifaces

downloads_dir = None

def render_qr_code(addr):
    """Generates a QR Code for the IP address and 
    displays it on the terminal.
    """
    url = pyqrcode.create(str(addr))
    url.svg("addr.svg", scale=8)
    url.eps("addr.eps", scale=2)
    print(url.terminal(quiet_zone=1))

def create_downloads_folder():
    """Checks if a `~/Downloads` dir is present. If not
    it creates one.
    """
    downloads_dir = os.path.join(os.environ['HOME'], 'Downloads')
    if not os.path.exists(downloads_dir):
        os.mkdir(downloads_dir)
    return downloads_dir

def human(data):
    """Decodes byte string into human readable format
    """
    return data.decode("utf-8")

def run(port=9000):
    """Opens up a socket connection on the port requested.
    If no value of port is supplied, port 9000 is used.
    """
    host = get_ip()
    print('Connect to {}:{}'.format(host, port))
    print('Scan the QR Code to connect :)')
    render_qr_code("{}:{}".format(host, port))
    try:
        connect_and_recv(host, port)
    except (KeyboardInterrupt, Exception) as e:
        print(e)
        print("Server stopped !")

def get_ip():
    """Returns the IP address .
    """
    return str(netifaces.ifaddresses("en0")[netifaces.AF_INET][0]['addr'])

def connect_and_recv(host, port):
    """Starts a socket server and waits 
    for connection and recieve files.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.listen(1)
    except Exception:
        s.close()
    while 1:
        conn, addr = s.accept()
        try:
            print("Connected by {}".format(addr))
            filename = str(conn.recv(1024).decode('utf-8')).rstrip('\n')
            print("Receiving : ", filename)
        except Exception as e:
            print("Could not recv filename !")              
        finally:
            conn.close()

        conn, addr = s.accept()
        try:
            receive_file(conn, filename)
        except Exception as e:
            print("Could not recv file !")
        finally:
            conn.close()

def receive_file(conn, filename):
    """Recieves  a file byte by byte over
    the connection.
    """
    f = open(os.path.join(downloads_dir, filename), 'wb')
    data = conn.recv(1024)
    while data:
        f.write(data)
        data = conn.recv(1024)
    f.close()
    print("File received successfully !")


if __name__ == "__main__":
    art = """
           _        _____                  
     /\   (_)      |  __ \                 
    /  \   _ _ __  | |  | |_ __ ___  _ __  
   / /\ \ | | '__| | |  | | '__/ _ \| '_ \ 
  / ____ \| | |    | |__| | | | (_) | |_) |
 /_/    \_\_|_|    |_____/|_|  \___/| .__/ 
                                    | |    
                                    |_|    
    """
    print("\033[93m {}\033[00m" .format(art))
    downloads_dir = create_downloads_folder()
    parser = argparse.ArgumentParser()
    parser.add_argument("-p")
    args = parser.parse_args()
    if args.p is not None:
        run(int(args.p))
    else:
        run()
