import socket
import requests
import AndroidTrustMatrix.config as Config


def open(connection,host,port):
    status = connection.connect((host,port))
    if status:
        return False 
    else:
        return True

def authenticate(connection,password):
    connection.send(b'AUTHENTICATE "' + password.encode('UTF-8') + b'"\n')
    recv = connection.recv(1024)
    if int(recv[0:3]) == 250:
        return True
    else:
        return False

def newnym(connection):
    connection.send(b'SIGNAL NEWNYM\n')
    recv = connection.recv(1024)
    if int(recv[0:3]) == 250:
        return True
    else:
        return False

def getnewip(proxies):
    r = requests.get("http://icanhazip.com",proxies=proxies)
    return r.text


def main():
    ip,port,password = Config.get_tor_admin()
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status = open(connection,ip,port)
    if not status:
        return False
    status = authenticate(connection,password)
    if not status:
        connection.close()
        return False
    status = newnym(connection)
    connection.close()
    return True
